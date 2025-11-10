# Multi-stage build for smaller final image
FROM python:3.12-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    librdkafka-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY pyproject.toml .
COPY ./poetry.lock .

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false  

# Install Python dependencies
RUN poetry install --no-root

# Final stage
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    librdkafka1 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY src/ ./src/

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Set Python to run in unbuffered mode for better logging
ENV PYTHONUNBUFFERED=1

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set the working directory to src where app.py is located
WORKDIR /app/src

# Run the application
CMD ["python", "-u", "app.py"]
