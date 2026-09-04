import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(dest_path: str, summary_data: dict, incidents_list: list):
    """Generates an executive-ready PDF summary log detailing discovered compromises."""
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    doc = SimpleDocTemplate(dest_path, pagesize=letter)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#990000'), spaceAfter=12)
    body_style = styles['Normal']
    
    story.append(Paragraph("RDRS Executive System Forensic Incident Report", title_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph(f"<b>Total Monitored Incidents Checked:</b> {summary_data.get('total_incidents', 0)}", body_style))
    story.append(Paragraph(f"<b>System Security Status:</b> {summary_data.get('status', 'EVALUATING')}", body_style))
    story.append(Spacer(1, 18))
    
    # Structural presentation table mapping
    table_data = [["Incident ID", "Threat Weighted Score", "Quarantine Evidence Target"]]
    for incident in incidents_list:
        table_data.append([str(incident.id), f"{incident.assigned_score}/100", str(incident.quarantine_path or 'None')])
        
    t = Table(table_data, colWidths=[100, 150, 250])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#333333')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F5F5F5')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ]))
    
    story.append(t)
    doc.build(story)
