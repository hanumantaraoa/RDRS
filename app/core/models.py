from pydantic import BaseModel
from datetime import datetime

class LocalFileEvent(BaseModel):
    event_type: str
    file_path: str
    timestamp: datetime
    file_extension: str