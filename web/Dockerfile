FROM python:3.11-slim

WORKDIR /app

RUN pip install flask

COPY app.py . 
COPY templates/ templates/


CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]

