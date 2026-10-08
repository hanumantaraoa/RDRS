from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database.connection import SessionLocal, DBAlert, DBFileEvent
import psutil
import os

router = APIRouter()
# Set correct file location path boundaries
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

@router.get("/", response_class=HTMLResponse)
async def render_dashboard(request: Request):
    db = SessionLocal()
    latest_alert = db.query(DBAlert).order_by(DBAlert.id.desc()).first()
    alerts = db.query(DBAlert).order_by(DBAlert.id.desc()).limit(10).all()
    events = db.query(DBFileEvent).order_by(DBFileEvent.id.desc()).limit(10).all()
    db.close()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "threat_level": latest_alert.severity_level if latest_alert else "Normal",
        "alerts": alerts,
        "events": events,
        "cpu_usage": psutil.cpu_percent()
    })