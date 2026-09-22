import os
import sys
import time
import random
import string
import requests
from loguru import logger

# Add root folder path to lookups to pull configuration mappings safely
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
from app.core.config import load_config

def generate_low_entropy_text(size=1024) -> bytes:
    """Generates highly predictable, low-entropy structural plain text data."""
    return ("A" * size).encode('utf-8')

def generate_high_entropy_bytes(size=1024) -> bytes:
    """Generates high-entropy random blocks mirroring encrypted files."""
    return os.urandom(size)

def run_simulation():
    logger.info("? Initializing Controlled Behavioral Ransomware Simulation script...")
    
    # 1. Resolve Target Operational Configuration Context Paths
    try:
        config = load_config("rdrs/config.yaml")
        sandbox_dir = config.system.monitored_directory
        api_url = f"http://{config.api.host}:{config.api.port}/api"
    except Exception as e:
        logger.error(f"Failed to bootstrap configuration configurations: {e}")
        return

    logger.info(f"?? Target Execution Sandbox Path: {sandbox_dir}")
    logger.info(f"?? Target System API Surface Endpoint: {api_url}")

    # Stage 0: Create standard base assets inside the workspace path
    test_files = []
    logger.info("?? Phase 1: Generating standard user structural document assets...")
    for i in range(5):
        fpath = os.path.join(sandbox_dir, f"financial_document_00{i}.docx")
        with open(fpath, "wb") as f:
            f.write(generate_low_entropy_text(2048))
        test_files.append(fpath)
    
    # Allow filesystem events to catch up
    time.sleep(2)

    # Stage 1: Execute Rapid Encrypted Actions Payload (Simulating Ransomware Loop)
    logger.info("?? Phase 2: Simulating rapid high-entropy modification & ransom extension lock sweep...")
    try:
        for idx, path in enumerate(test_files):
            if not os.path.exists(path):
                continue
            
            logger.warning(f"?? Compromising file: {os.path.basename(path)}")
            
            # Step A: Rewrite file data bytes with high-entropy encrypted block variations (FR-3, FR-7)
            with open(path, "wb") as f:
                f.write(generate_high_entropy_bytes(4096))
            
            # Step B: Alter file extension to mimicking common ransomware signatures (.locked) (FR-2)
            locked_path = path.replace(".docx", ".locked")
            os.rename(path, locked_path)
            
            # Rapid execution window throttle mimicking automated programmatic speeds
            time.sleep(0.15)
            
    except Exception as ex:
        logger.error(f"Error encountered during simulation sequence execution: {ex}")

    # Allow processing loop context time window to compute scores and save alerts
    logger.info("? Waiting for sliding evaluation windows processing cycles to conclude...")
    time.sleep(3)

    # Stage 2: Audit endpoint telemetry collection records directly from REST API
    logger.info("?? Phase 3: Inspecting system behavior records using REST API endpoints...")
    try:
        alerts_resp = requests.get(f"{api_url}/alerts", timeout=3)
        incidents_resp = requests.get(f"{api_url}/incidents", timeout=3)
        
        if alerts_resp.status_code == 200:
            alerts = alerts_resp.json()
            logger.info(f"?? Live API Alerts Extracted count: {len(alerts)}")
            for a in alerts[:3]:
                logger.success(f"[API CHECK] Registered Alert ID: {a['id']} | Computed Score: {a['threat_score']} | Details: {a['description']}")
        
        if incidents_resp.status_code == 200:
            incidents = incidents_resp.json()
            logger.info(f"??? Live API Active Containment Records count: {len(incidents)}")
            for inc in incidents[:3]:
                logger.success(f"[API CHECK] Incident ID: {inc['id']} | Action Path: {inc['quarantine_path']}")
                
    except requests.exceptions.ConnectionError:
        logger.error("? Unable to connect to REST API engine service. Ensure 'python rdrs/app/main.py' is actively running.")

if __name__ == "__main__":
    run_simulation()