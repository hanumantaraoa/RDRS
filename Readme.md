# Ransomware Detection and Response System (RDRS)

Heuristic-driven defensive cybersecurity platform monitoring file-system activity and compute matrices.

## Deployment with Docker
```bash
docker compose up --build
```
Access the dark-theme security dashboard directly at: `http://127.0.0.1:8000/`
Examine Swagger OpenAPI specs at: `http://127.0.0.1:8000/docs`

## Local CLI Validation Framework
```bash
pip install -r requirements.txt
pytest --cov=app tests/
```