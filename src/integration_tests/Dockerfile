FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD ["pytest", "-v", "src/integration_tests/test_etl.py"]