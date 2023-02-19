FROM python:3.11-slim-bullseye

WORKDIR /opt/dosuri

COPY requirements.txt ./

RUN apt-get update && \
    apt-get install -y build-essential libpq-dev --no-install-recommends && \
    python3 -m pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn psycopg2 && \
    apt-get purge -y --auto-remove build-essential

CMD ["gunicorn", "--workers=2", "maf_core.site.wsgi:application", "--bind=0.0.0.0:8000"]
