from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProcessTelemetry(BaseModel):
    pid: Optional[int]
    name: str
    exe: str
    username: str

class FileEventModel(BaseModel):
    event_type: str
    src_path: str
    dest_path: Optional[str] = None
    timestamp: datetime
    entropy: float = 0.0
    pid: Optional[int] = None
    process_name: Optional[str] = None
