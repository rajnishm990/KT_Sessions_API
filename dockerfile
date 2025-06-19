FROM python:3.11-slim

WORKDIR /app/backend
COPY ./backend /app/backend
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python manage.py 

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]