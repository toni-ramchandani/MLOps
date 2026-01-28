FROM python:3.12-slim

LABEL maintainer="MLOps Enterprise <team@example.com>"
LABEL description="Enterprise-grade MLOps API service"

WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 mlops && \
    mkdir -p /app/logs && \
    chown -R mlops:mlops /app

# Install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir -e . && \
    pip install --no-cache-dir \
    gunicorn \
    python-json-logger

# Copy application code
COPY --chown=mlops:mlops . .

# Switch to non-root user
USER mlops

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "mlops_enterprise.api:app", "--host", "0.0.0.0", "--port", "8000"]
