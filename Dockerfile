FROM python:3.11-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local
COPY . /app
COPY docker_entrypoint.py /app/docker_entrypoint.py

RUN pip install gunicorn

EXPOSE 8000

ENTRYPOINT ["python", "docker_entrypoint.py"]