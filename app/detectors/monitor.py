import os
import sys
import psutil
from datetime import datetime
from pathlib import Path
from loguru import logger
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.core.config import AppConfig
from app.core.entropy import calculate_shannon_entropy
from app.core.models import LocalFileEvent
from app.database.connection import SessionLocal, DBFileEvent, DBProcess

class SystemTelemetryHandler(FileSystemEventHandler):
    def __init__(self, config: AppConfig, analyzer):
        self.config = config
        self.analyzer = analyzer
        self.event_counter = 0

    def on_any_event(self, event):
        if event.is_directory:
            return

        event_map = {"created": "create", "modified": "modify", "deleted": "delete", "moved": "rename"}
        etype = event_map.get(event.event_type)
        if not etype:
            return

        src = event.src_path
        if self.config.monitor.quarantine_path in src:
            return

        self.event_counter += 1
        sys.stdout.write(f"\r[LIVE MONITOR] Total Events Caught: {self.event_counter}")
        sys.stdout.flush()

        local_obj = LocalFileEvent(
            event_type=etype,
            file_path=src,
            timestamp=datetime.utcnow(),
            file_extension=Path(src).suffix
        )
        logger.bind(channel="events").info(f"Event: {local_obj.event_type} | Path: {local_obj.file_path}")

        dest = getattr(event, "dest_path", None)
        entropy_val = calculate_shannon_entropy(src) if etype in ("create", "modify") else None
        pid = os.getpid()

        self._record_telemetry(etype, src, dest, entropy_val, pid)
        self.analyzer.evaluate_window()

    def _record_telemetry(self, etype, src, dest, entropy, pid):
        db = SessionLocal()
        try:
            if pid and not db.query(DBProcess).filter(DBProcess.pid == pid).first():
                try:
                    p = psutil.Process(pid)
                    db.add(DBProcess(pid=pid, name=p.name(), exe=p.exe(), cmdline=" ".join(p.cmdline()), username=p.username()))
                except Exception:
                    pass
            db.add(DBFileEvent(event_type=etype, src_path=src, dest_path=dest, entropy=entropy, pid=pid))
            db.commit()
        except Exception as e:
            logger.bind(channel="system").error(f"Failed committing logs: {e}")
        finally:
            db.close()

def orchestrate_monitor(config: AppConfig, analyzer) -> Observer:
    observer = Observer()
    handler = SystemTelemetryHandler(config, analyzer)
    for path_str in config.monitor.watch_paths:
        Path(path_str).mkdir(parents=True, exist_ok=True)
        observer.schedule(handler, path=path_str, recursive=True)
    observer.start()
    return observer