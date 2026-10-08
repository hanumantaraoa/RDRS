import csv
import json
import os
from app.database.connection import SessionLocal, DBIncident
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def compile_reports(output_base: str = "data/incident_report"):
    db = SessionLocal()
    incidents = db.query(DBIncident).order_by(DBIncident.id.desc()).all()
    db.close()

    if not incidents:
        return

    top = incidents[0]
    payload = {
        "timestamp": str(top.timestamp),
        "threat_score": top.score,
        "suspect_process": top.suspect_process,
        "affected_files": top.affected_files.split(";"),
        "recommendations": ["Isolate node immediately", "Revoke credentials", "Verify backup validation layers"]
    }

    # 1. Output JSON execution
    with open(f"{output_base}.json", "w") as f:
        json.dump(payload, f, indent=2)

    # 2. Output CSV execution
    with open(f"{output_base}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Metric Name", "Telemetry Realignment Log Data"])
        writer.writerow(["Timestamp", payload["timestamp"]])
        writer.writerow(["Threat Score", f"{payload['threat_score']}%"])
        writer.writerow(["Suspect Process Context", payload["suspect_process"]])
        writer.writerow(["Impacted Files Aggregate Count", len(payload["affected_files"])])

    # 3. Output ReportLab PDF Layout Implementation
    doc = SimpleDocTemplate(f"{output_base}.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("RDRS Automated Incident Forensics Report", styles["Heading1"]),
        Spacer(1, 12),
        Paragraph(f"Threat Score Evaluation: {payload['threat_score']}%", styles["Heading3"]),
        Paragraph(f"Suspect Target Component: {payload['suspect_process']}", styles["Normal"]),
        Spacer(1, 10)
    ]
    
    table_data = [["Affected File Paths System Mapping Layer"]]
    for path in payload["affected_files"][:10]:
        table_data.append([path])
        
    t = Table(table_data, colWidths=[400])
    t.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.red), ('BACKGROUND', (0,0), (-1,0), colors.gray)]))
    story.append(t)
    doc.build(story)