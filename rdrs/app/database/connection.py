from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class DBFileEvent(Base):
    __tablename__ = 'file_events'
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String, nullable=False)
    src_path = Column(String, nullable=False)
    dest_path = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    entropy = Column(Float, default=0.0)
    pid = Column(Integer, nullable=True)
    process_name = Column(String, nullable=True)

class DBProcess(Base):
    __tablename__ = 'processes'
    pid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    exe = Column(String, nullable=True)
    username = Column(String, nullable=True)
    captured_at = Column(DateTime, default=datetime.utcnow)

class DBAlert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    threat_score = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    trigger_pid = Column(Integer, nullable=True)

class DBIncident(Base):
    __tablename__ = 'incidents'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="ACTIVE")
    assigned_score = Column(Float, nullable=False)
    quarantine_path = Column(String, nullable=True)

def init_db(db_url: str):
    engine = create_engine(db_url, connect_args={"check_same_thread": False} if "sqlite" in db_url else {})
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
