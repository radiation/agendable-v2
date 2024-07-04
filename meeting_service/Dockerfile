FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app
COPY ./alembic /app/alembic
COPY ./alembic.ini /app/alembic.ini
COPY ./run_migrations.sh /app/run_migrations.sh

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
