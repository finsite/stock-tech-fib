# ---- Stage 1: Builder Image ----
FROM python:3.13-slim AS builder

WORKDIR /app

# Install system dependencies (only if needed for certain packages)
RUN apt-get update && \
apt-get install --no-install-recommends -y \
    gcc \
    libffi-dev && \
rm -rf /var/lib/apt/lists/*    

# Copy only `requirements.txt` for better caching
COPY requirements.txt .

# Install dependencies into isolated path
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---- Stage 2: Final Runtime Image ----
FROM python:3.13-slim

WORKDIR /app

# Copy Python packages from builder image
COPY --from=builder /install /usr/local

# Copy source code
COPY src /app/src

# Set Python path for module resolution
ENV PYTHONPATH="/app"

# Create a non-root user
RUN useradd -m appuser && chown -R appuser /app

# Switch to non-root user
USER appuser

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
CMD pgrep -f "main.py" > /dev/null || exit 1

# Start the app
CMD ["python", "/app/src/main.py"]
