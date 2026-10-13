FROM python:3.9-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=5000
ENV FITNESS_DATABASE=/app/instance/fitness.db

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ ./templates/
COPY static/ ./static/
COPY tests/ ./tests/

RUN mkdir -p /app/instance

EXPOSE 5000

CMD ["python", "app.py"]
