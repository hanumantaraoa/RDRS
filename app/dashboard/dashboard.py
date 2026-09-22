from fastapi.responses import HTMLResponse
from jinja2 import Template

def get_dashboard_html(events, alerts) -> HTMLResponse:
    # Embedded dynamic Jinja2 view interface page template
    template_str = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>RDRS Defense Center Monitor Panel</title>
        <meta http-equiv="refresh" content="3">
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 30px; background-color: #0f172a; color: #e2e8f0; }
            h1 { color: #f43f5e; border-bottom: 2px solid #334155; padding-bottom: 10px; }
            .grid { display: flex; gap: 20px; }
            .section { flex: 1; background: #1e293b; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.5); }
            table { width: 100%; border-collapse: collapse; margin-top: 15px; }
            th, td { text-align: left; padding: 10px; border-bottom: 1px solid #334155; font-size: 13px; }
            th { background-color: #334155; color: #f8fafc; }
            .badge-alert { background-color: #ef4444; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>🛡️ RDRS Ransomware Security Defense Control Center</h1>
        <p>Live endpoint monitoring activity streams active. Interface auto-refreshes every 3s.</p>
        <div class="grid">
            <div class="section">
                <h2>⚠️ Security Countermeasures Alerts Logs</h2>
                <table>
                    <tr><th>ID</th><th>Score</th><th>Trigger PID</th><th>Description</th></tr>
                    {% for a in alerts %}
                    <tr>
                        <td>{{ a.id }}</td>
                        <td><span class="badge-alert">{{ a.threat_score }}</span></td>
                        <td>{{ a.trigger_pid }}</td>
                        <td>{{ a.description }}</td>
                    </tr>
                    {% endfor %}
                </table>
            </div>
            <div class="section">
                <h2>📊 Telemetry Streaming Events Tracked</h2>
                <table>
                    <tr><th>Type</th><th>Target File Source Path</th><th>Entropy</th><th>Process Context</th></tr>
                    {% for e in events %}
                    <tr>
                        <td><strong>{{ e.event_type }}</strong></td>
                        <td>{{ e.src_path }}</td>
                        <td>{{ e.entropy }}</td>
                        <td>{{ e.process_name }} ({{ e.pid }})</td>
                    </tr>
                    {% endfor %}
                </table>
            </div>
        </div>
    </body>
    </html>
    """
    t = Template(template_str)
    return HTMLResponse(content=t.render(events=events, alerts=alerts))
