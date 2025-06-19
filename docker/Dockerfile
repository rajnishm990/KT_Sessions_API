FROM python:3.11-slim

WORKDIR /app

# Copy requirements from backend directory
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory to /app
COPY backend/ .


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]