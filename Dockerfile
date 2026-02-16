FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root --only main \
    && pip uninstall -y poetry poetry-core poetry-plugin-export \
    && rm -rf /root/.cache/pypoetry /root/.cache/pip

COPY . .

EXPOSE 5000

CMD flask db upgrade && gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120 --max-requests 1000 --max-requests-jitter 50 run:app
