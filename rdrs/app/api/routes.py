from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import DBFileEvent, DBAlert, DBIncident, DBProcess

router = APIRouter()
_session_maker = None

def init_api_session(session_maker):
    global _session_maker
    _session_maker = session_maker

def get_db():
    session = _session_maker()
    try:
        yield session
    finally:
        session.close()

@router.get("/health")
def get_health():
    return {"status": "HEALTHY", "engine": "RDRS Operational Monitoring Core active"}

@router.get("/events")
def get_events(limit: int = 100, db: Session = Depends(get_db)):
    """FR-10: Exposes tracked real-time file transaction telemetry logs."""
    return db.query(DBFileEvent).order_by(DBFileEvent.id.desc()).limit(limit).all()

@router.get("/processes")
def get_processes(db: Session = Depends(get_db)):
    return db.query(DBProcess).all()

@router.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    """FR-10: Exposes generated threat security alerts details."""
    return db.query(DBAlert).order_by(DBAlert.id.desc()).all()

@router.get("/incidents")
def get_incidents(db: Session = Depends(get_db)):
    return db.query(DBIncident).order_by(DBIncident.id.desc()).all()
