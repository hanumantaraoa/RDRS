import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from loguru import logger
from app.core.config import AppConfig
from app.database.connection import SessionLocal, DBFileEvent, DBAlert, DBIncident, DBProcess

class ThreatAnalyzer:
    def __init__(self, config: AppConfig):
        self.config = config

    def evaluate_window(self):
        db = SessionLocal()
        try:
            now = datetime.utcnow()
            window_start = now - timedelta(seconds=self.config.monitor.window_seconds)
            events = db.query(DBFileEvent).filter(DBFileEvent.timestamp >= window_start).all()
            if not events:
                return

            score = 0.0
            w = self.config.weights
            
            # 1. Rapid encryption heuristic match
            mod_count = sum(1 for e in events if e.event_type in ("create", "modify"))
            if mod_count >= self.config.monitor.max_events_per_window:
                score += w.rapid_encryption
                
            # 2. Mass rename logic
            rename_count = sum(1 for e in events if e.event_type == "rename")
            if rename_count >= 5:
                score += w.mass_rename

            # 3. High entropy thresholds evaluation
            high_ent_count = sum(1 for e in events if e.entropy and e.entropy >= self.config.monitor.entropy_threshold)
            if high_ent_count >= 3:
                score += w.high_entropy

            # 4. Global process metrics extraction simulation context
            pids = list({e.pid for e in events if e.pid})
            suspect_proc_str = "Unknown"
            if pids:
                proc_record = db.query(DBProcess).filter(DBProcess.pid == pids[0]).first()
                if proc_record:
                    suspect_proc_str = f"{proc_record.name} (PID: {proc_record.pid})"

            # Cap the score matrix bounds
            score = min(score, 100.0)
            
            # Map level boundaries
            if score <= 40.0:
                level = "Normal"
            elif score <= 70.0:
                level = "Warning"
            else:
                level = "Critical"

            if level in ("Warning", "Critical"):
                desc = f"Heuristic matches triggered: {len(events)} events inside sliding window."
                alert = DBAlert(threat_score=score, severity_level=level, description=desc, pid=pids[0] if pids else None)
                db.add(alert)
                db.commit()
                logger.bind(channel="alerts").warning(f"[ALERT] Threat Level: {level} | Score: {score}%")

            if level == "Critical":
                self._handle_critical_incident(db, score, events, suspect_proc_str)
        except Exception as e:
            logger.bind(channel="system").error(f"Error executing sliding threat score window: {e}")
        finally:
            db.close()

    def _handle_critical_incident(self, db, score: float, events, suspect_proc: str):
        affected_paths = list({e.src_path for e in events})
        incident = DBIncident(
            score=score,
            suspect_process=suspect_proc,
            affected_files=";".join(affected_paths)
        )
        db.add(incident)
        db.commit()

        logger.bind(channel="audit").info(f"[INCIDENT AUDIT] Critical containment executed. Suspect process: {suspect_proc}")

        # Execute quarantine replication logic safely
        quar_dir = Path(self.config.monitor.quarantine_path)
        quar_dir.mkdir(parents=True, exist_ok=True)
        for path_str in affected_paths:
            src = Path(path_str)
            if src.is_file() and src.exists():
                try:
                    dest = quar_dir / f"{src.name}_{int(datetime.utcnow().timestamp())}"
                    shutil.copy2(src, dest)
                except Exception:
                    pass

        # Execution Simulation Logic verification
        if self.config.monitor.simulation_mode:
            logger.bind(channel="audit").info(f"[SIMULATION] Would terminate hostile process context: {suspect_proc}")