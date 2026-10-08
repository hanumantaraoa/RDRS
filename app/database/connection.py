import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///data/rdrs.db"
os.makedirs("data", exist_ok=True)

Engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)
Base = declarative_base()

class DBFileEvent(Base):
    __tablename__ = "file_events"
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, nullable=False)
    src_path = Column(String, nullable=False)
    dest_path = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    entropy = Column(Float, nullable=True)
    pid = Column(Integer, nullable=True)

class DBProcess(Base):
    __tablename__ = "processes"
    pid = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    exe = Column(String, nullable=True)
    cmdline = Column(String, nullable=True)
    username = Column(String, nullable=True)

class DBAlert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    threat_score = Column(Float, nullable=False)
    severity_level = Column(String, nullable=False)
    description = Column(String, nullable=False)
    pid = Column(Integer, nullable=True)

class DBIncident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    score = Column(Float, nullable=False)
    suspect_process = Column(String, nullable=True)
    affected_files = Column(String, nullable=False)

def init_db():
    Base.metadata.create_all(bind=Engine)