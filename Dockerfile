# ---- Stage 1: Build ----    
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    build-essential \
    gcc \
    g++ \
    libffi-dev \
    libatlas-base-dev \
    libopenblas-dev \
    liblapack-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---- Stage 2: Final Minimal Image ----
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local
COPY src /app/src

ENV PYTHONPATH="/app"

RUN useradd -m appuser && chown -R appuser /app
USER appuser

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD pgrep -f "app.main" > /dev/null || exit 1

CMD ["python", "-m", "app.main"]
