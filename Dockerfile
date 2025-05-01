FROM python:3.13-slim AS builder

WORKDIR /app

# Install build dependencies for numpy, pandas, etc.
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

# Copy requirements and install packages to /install
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---- Stage 2: Final Minimal Image ----
FROM python:3.13-slim

WORKDIR /app

# Install runtime dependencies only (no build tools)
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only the built dependencies from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY src /app/src

# Set environment variables
ENV PYTHONPATH="/app"

# Create a non-root user
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Healthcheck for container monitoring
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD pgrep -f "main.py" > /dev/null || exit 1

# Corrected default startup command
CMD ["python", "-m", "app.main"]
