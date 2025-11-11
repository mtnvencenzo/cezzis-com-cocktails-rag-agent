# Multi-stage build for smaller final image
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

# Install system dependencies required for building Python packages
# Builder stage - need dev libraries to compile confluent-kafka
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    librdkafka-dev \
    && rm -rf /var/lib/apt/lists/*

# Setup poetry for build and dependency management
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create true

# Copy application code
COPY ./pyproject.toml ./src/
COPY ./poetry.lock ./src/
COPY ./README.md ./src/
COPY ./data_ingestion_agentic_workflow/ ./src/data_ingestion_agentic_workflow/

# Build the application
WORKDIR /app/src
RUN poetry install
RUN poetry build -o dist -v

# Final stage
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    librdkafka1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the built package from builder
COPY --from=builder /app/src/dist/data_ingestion_agentic_workflow-0.0.1.tar.gz ./

# Install the package
RUN pip install --no-cache-dir data_ingestion_agentic_workflow-0.0.1.tar.gz

# Set Python to run in unbuffered mode for better logging
ENV PYTHONUNBUFFERED=1

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set the working directory to dist where app.py is located
WORKDIR /app/dist

# Run the application using the installed package
CMD ["python", "-m", "data_ingestion_agentic_workflow.app"]
