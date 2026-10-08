import pytest
from app.core.entropy import calculate_shannon_entropy
from app.core.config import AppConfig
from app.database.connection import SessionLocal, init_db, DBFileEvent, DBIncident
from app.detectors.engine import ThreatAnalyzer

def test_entropy_pure_logic():
    assert calculate_shannon_entropy("non_existent_file.enc") == 0.0

def test_pipeline_integration_critical_burst(tmp_path):
    init_db()
    db = SessionLocal()
    
    # Inject burst of events simulating rapid high-threat activity
    for i in range(20):
        evt = DBFileEvent(
            event_type="create",
            src_path=str(tmp_path / f"canary_file_{i}.lock"),
            entropy=7.9
        )
        db.add(evt)
    db.commit()

    config = AppConfig()
    config.monitor.max_events_per_window = 5
    
    analyzer = ThreatAnalyzer(config)
    analyzer.evaluate_window()

    # Confirm score calculation limits and incident processing logic
    incident = db.query(DBIncident).order_by(DBIncident.id.desc()).first()
    assert incident is not None
    assert incident.score >= 70.0
    db.close()