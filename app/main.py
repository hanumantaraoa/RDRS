import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import load_config
from app.core.logging import setup_multichannel_logging
from app.database.connection import init_db
from app.detectors.engine import ThreatAnalyzer
from app.detectors.monitor import orchestrate_monitor
from app.api.routes import router as api_router
from app.dashboard.server import router as web_router
from app.reports.generator import compile_reports

config = load_config()
analyzer = ThreatAnalyzer(config)
observer_ctx = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global observer_ctx
    setup_multichannel_logging()
    init_db()
    observer_ctx = orchestrate_monitor(config, analyzer)
    yield
    if observer_ctx:
        observer_ctx.stop()
        observer_ctx.join()
    compile_reports()

app = FastAPI(title="RDRS Cybersecurity Platform Engine", lifespan=lifespan)
app.include_router(web_router)
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host=config.server.host, port=config.server.port)