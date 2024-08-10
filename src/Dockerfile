FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    make \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.in requirements.txt .flake8 /app/

RUN pip install --upgrade pip \
 && pip install pip-tools \
 && pip-compile requirements.in \
 && pip install -r requirements.txt

ARG COMMIT=local-commit
ENV COMMIT=$COMMIT
ENV PORT=1000

# Add util that checks if other containers are ready before running tests
COPY --from=ghcr.io/ufoscout/docker-compose-wait:latest /wait /wait

CMD sh -c "/wait \
            && uvicorn --host 0.0.0.0 --port $PORT smart_cart.main:app"