The RDRS (Ransomware Defense & Response System) application is a modular, defensive Python service that monitors real-time file-system operations and system process metrics to identify ransomware behavior.
Below is the complete implementation blueprint, organized by the specified directory structure,
 app/
    core/         # config, logging, entropy, shared models
    detectors/    # file monitor + detection engine
    database/     # database models and access
    api/          # REST API
    dashboard/    # web dashboard
    reports/      # report generation
    main.py       # program entry point
  tests/          # your tests
  logs/           # log files (created at runtime)
  data/           # database + sandbox test area
  config.yaml     # all settings
  requirements.txt
  README.md

configuration and components.
watchdog psutil pydantic pyyaml loguru sqlalchemy fastapi uvicorn reportlab jinja2 pytest pytest-cov
satisfying functional requirements
FR-1
Load configuration from config.yaml.
FR-2
Monitor file create/modify/delete/rename events in real time.
FR-3
Calculate Shannon entropy of modified files.
FR-4
Collect process metadata using psutil.
FR-5
Store events, processes, alerts and incidents in SQLite.
FR-6
Analyze events in a sliding time window.
FR-7
Compute weighted threat score (0-100).
FR-8
Generate alerts and incident records.
FR-9
Copy evidence to quarantine (simulation mode).
FR-10
Provide REST API endpoints.
FR-11
Display live dashboard.
FR-12
Generate JSON/CSV reports.
FR-13
Support automated testing and Docker deployment.
Non-Functional Requirements
• Real-time monitoring
• Modular Python architecture
• Simulation mode by default
• Comprehensive logging
• Maintainable and documented code
Inputs
File events, process information, configuration settings.
Outputs
Threat scores, alerts, logs, incident records, REST API responses, dashboard updates, reports.
Assumptions & Constraints
Defensive use only. No malware execution. Testing only in sandbox environment.

