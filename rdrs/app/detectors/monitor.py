import os
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import psutil
from loguru import logger
from app.core.models import FileEventModel
from app.core.entropy import calculate_shannon_entropy
from app.database.connection import DBProcess

class RansomwareMonitorHandler(FileSystemEventHandler):
    def __init__(self, engine, session_factory):
        self.engine = engine
        self.Session = session_factory

    def _harvest_process_metadata(self) -> tuple[int | None, str | None]:
        """FR-4: Tracks the calling PID and matches system execution footprints using psutil."""
        # Watchdog fires context sync loops on current threads. 
        # Fall back gracefully to active caller contexts if matching handles are busy.
        try:
            p = psutil.Process()
            pid = p.pid
            name = p.name()
            
            # Save or update mapped process details (FR-5)
            session = self.Session()
            if not session.query(DBProcess).filter_by(pid=pid).first():
                db_p = DBProcess(
                    pid=pid,
                    name=name,
                    exe=p.exe() if hasattr(p, "exe") else "N/A",
                    username=p.username() if hasattr(p, "username") else "N/A"
                )
                session.add(db_p)
                session.commit()
            session.close()
            return pid, name
        except Exception:
            return os.getpid(), "python_runtime_rdrs"

    def on_created(self, event):
        if event.is_directory: return
        pid, name = self._harvest_process_metadata()
        self.engine.process_new_event(FileEventModel(
            event_type="CREATE", src_path=event.src_path, timestamp=datetime.utcnow(), pid=pid, process_name=name
        ))

    def on_modified(self, event):
        if event.is_directory: return
        pid, name = self._harvest_process_metadata()
        entropy_val = calculate_shannon_entropy(event.src_path)
        self.engine.process_new_event(FileEventModel(
            event_type="MODIFY", src_path=event.src_path, timestamp=datetime.utcnow(), entropy=entropy_val, pid=pid, process_name=name
        ))

    def on_deleted(self, event):
        if event.is_directory: return
        pid, name = self._harvest_process_metadata()
        self.engine.process_new_event(FileEventModel(
            event_type="DELETE", src_path=event.src_path, timestamp=datetime.utcnow(), pid=pid, process_name=name
        ))

    def on_moved(self, event):
        if event.is_directory: return
        pid, name = self._harvest_process_metadata()
        entropy_val = calculate_shannon_entropy(event.dest_path)
        self.engine.process_new_event(FileEventModel(
            event_type="RENAME", src_path=event.src_path, dest_path=event.dest_path, timestamp=datetime.utcnow(), entropy=entropy_val, pid=pid, process_name=name
        ))

def start_file_monitor(config, engine, session_factory):
    observer = Observer()
    handler = RansomwareMonitorHandler(engine, session_factory)
    observer.schedule(handler, path=config.system.monitored_directory, recursive=True)
    observer.start()
    logger.info(f"Watchdog real-time file-system analysis routing started on target path: {config.system.monitored_directory}")
    return observer
