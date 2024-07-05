FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to /app
COPY ./app /app

# Copy Alembic and migration scripts to a separate directory
COPY ./alembic /migrations/alembic
COPY ./alembic.ini /migrations/alembic.ini
COPY ./run_migrations.sh /migrations/run_migrations.sh

ENV PYTHONPATH=/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
