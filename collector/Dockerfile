FROM python:3.11-slim 

WORKDIR /app

RUN pip install pyserial python-dotenv

COPY main.py . 

CMD ["python", "main.py"]
