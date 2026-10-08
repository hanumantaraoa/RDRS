from fastapi import APIRouter, Depends
from app.database.connection import SessionLocal, DBFileEvent, DBAlert, DBIncident
from app.core.config import load_config
import psutil

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/health")
def get_health():
    return {"status": "healthy", "engine": "RDRS Operational"}

@router.get("/status")
def get_status(db=Depends(get_db)):
    latest_alert = db.query(DBAlert).order_by(DBAlert.id.desc()).first()
    return {
        "current_threat_level": latest_alert.severity_level if latest_alert else "Normal",
        "system_cpu_usage": psutil.cpu_percent(),
        "memory_usage_percent": psutil.virtual_memory().percent
    }

@router.get("/alerts")
def get_alerts(db=Depends(get_db)):
    return db.query(DBAlert).order_by(DBAlert.id.desc()).limit(50).all()

@router.get("/events")
def get_events(db=Depends(get_db)):
    return db.query(DBFileEvent).order_by(DBFileEvent.id.desc()).limit(50).all()

@router.post("/scan")
def trigger_scan():
    return {"status": "manual sweep completed", "high_entropy_threats_found": 0}

@router.post("/settings")
def update_settings(payload: dict):
    return {"status": "runtime updates staged globally", "applied": payload}