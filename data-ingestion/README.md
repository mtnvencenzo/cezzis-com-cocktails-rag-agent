# Cezzis.com Cocktails RAG - Data Extraction Agent

> Part of the broader Cezzis.com RAG solution for semantic search and AI-powered cocktail discovery.

[![CI](https://github.com/mtnvencenzo/cezzis-com-cocktails-rag-agent/actions/workflows/cezzis-rag-data-extraction-cicd.yaml/badge.svg?branch=main)](https://github.com/mtnvencenzo/cezzis-com-cocktails-rag-agent/actions/workflows/cezzis-rag-data-extraction-cicd.yaml)
[![Release](https://img.shields.io/github/v/release/mtnvencenzo/cezzis-com-cocktails-rag-agent?include_prereleases)](https://github.com/mtnvencenzo/cezzis-com-cocktails-rag-agent/releases)
[![License](https://img.shields.io/badge/license-Proprietary-lightgrey)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)
[![Last commit](https://img.shields.io/github/last-commit/mtnvencenzo/cezzis-com-cocktails-rag-agent?branch=main)](https://github.com/mtnvencenzo/cezzis-com-cocktails-rag-agent/commits/main)
[![Issues](https://img.shields.io/github/issues/mtnvencenzo/cezzis-com-cocktails-rag-agent)](https://github.com/mtnvencenzo/cezzis-com-cocktails-rag-agent/issues)
[![Project](https://img.shields.io/badge/project-Cezzis.com%20Cocktails-181717?logo=github&logoColor=white)](https://github.com/users/mtnvencenzo/projects/2)
[![Website](https://img.shields.io/badge/website-cezzis.com-2ea44f?logo=google-chrome&logoColor=white)](https://www.cezzis.com)


A Kafka consumer application that processes cocktail data updates in real-time as part of the Cezzis.com RAG (Retrieval-Augmented Generation) solution. This agent listens for cocktail updates, extracts relevant data, and prepares it for vectorization and semantic search indexing.


# Running Docker Local
```bash
docker build -t cezzis-ingestion-agentic-workflow:latest .

docker run -d \
  --env ENV="local" \
  --name cezzis-ingestion-agentic-workflow \
  --network=host cezzis-ingestion-agentic-workflow:latest

```







## 🧩 Cezzis.com RAG Ecosystem

This application is part of a multi-service RAG solution:

- **data-extraction-agent** (this app) – Kafka consumer that processes cocktail data updates
- **vector-storage** *(coming soon)* – Manages vector embeddings and similarity search
- **query-processor** *(coming soon)* – Handles semantic search queries and retrieval
- **rag-orchestrator** *(coming soon)* – Coordinates retrieval and generation for AI responses

Related repositories:
- [**cocktails-api**](https://github.com/mtnvencenzo/cezzis-com-cocktails-api) – ASP.NET Core backend and REST API
- [**cocktails-mcp**](https://github.com/mtnvencenzo/cezzis-com-cocktails-mcp) – Model Context Protocol server for AI agents
- [**cocktails-web**](https://github.com/mtnvencenzo/cezzis-com-cocktails-web) – React SPA for the public experience
- [**shared-infrastructure**](https://github.com/mtnvencenzo/shared-infrastructure) – Global Terraform modules

## ☁️ Cloud-Native Footprint (Azure)

Infrastructure is provisioned with Terraform and deployed into Azure:

- **Azure Container Apps** – Hosts the data extraction agent with auto-scaling
- **Azure Event Hubs / Kafka** – Event streaming platform for cocktail updates
- **Azure Container Registry** – Stores container images published from CI/CD
- **Azure Key Vault** – Holds secrets (Kafka credentials, API keys)
- **Azure Monitor** – Telemetry collection via OpenTelemetry and OTLP exporter
- **Azure AI Search** *(future)* – Vector storage and semantic search capabilities

## 🔄 Data Flow

```
Cocktails API → Kafka Topic → Data Extraction Agent → Vector Store → Semantic Search
                   ↑                     ↓
            (cocktails-topic)    (Extract, Transform, Validate)
```

1. **Ingest**: Cocktail updates published to Kafka topic
2. **Extract**: Agent consumes messages and extracts cocktail data
3. **Transform**: Data normalized and prepared for vectorization
4. **Validate**: Schema validation and quality checks
5. **Output**: Prepared data sent to vector storage service

## 🛠️ Technology Stack

### Core
- **Language**: Python 3.12+
- **Framework**: Pydantic for configuration and validation
- **Message Broker**: Apache Kafka via confluent-kafka
- **Logging**: Structured logging with Python logging module

### Integrations
- **Apache Kafka**: Event streaming platform for real-time data ingestion
- **Pydantic Settings**: Type-safe configuration management with environment variables
- **OpenTelemetry** *(future)*: Distributed tracing and observability

### Development
- **Testing**: pytest with pytest-mock for unit tests
- **Linting**: ruff for code formatting and linting
- **Type Checking**: Python type hints throughout codebase

## 🏗️ Project Structure

```text
data-extraction-agent/
├── data_ingestion_agentic_workflow/
│   ├── app.py                 # Main application entry point
│   ├── app_settings.py        # Configuration management
│   └── __pycache__/
├── test/
│   ├── test_app.py           # Application tests
│   ├── test_app_settings.py  # Configuration tests
│   └── __pycache__/
├── Dockerfile                # Production container image
├── Dockerfile-CI             # CI/CD optimized container
├── .dockerignore             # Docker build exclusions
├── .ruff.toml                # Ruff linter configuration
├── pytest.ini                # pytest configuration
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
├── makefile                  # Build automation
└── README.md                 # This file
```

## 🚀 Development Setup

### 1) Prerequisites
- Python 3.12 or newer
- Make (build automation)
- Docker and Docker Compose (for local Kafka)
- Optional: Azure CLI / Terraform (infrastructure)

### 2) Virtual Environment Setup
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

### 3) Install Dependencies
```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Or use Make
make install
```

### 4) Environment Configuration
Create a `.env` file in `./data-ingestion/data-extraction-agent/`:

```env
# Required: Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_CONSUMER_GROUP=extraction-group
KAFKA_TOPIC_NAME=cocktails-topic

# Optional: Logging
LOG_LEVEL=INFO

# Optional: OpenTelemetry (future)
OTEL_EXPORTER_OTLP_ENDPOINT=https://your-otlp-endpoint
OTEL_EXPORTER_OTLP_HEADERS=key1=value1,key2=value2
```

### 5) Run Locally
```bash
# Option 1: Direct Python execution
python data_ingestion_agentic_workflow/app.py

# Option 2: Using Make
make run

# Option 3: Docker Compose (includes local Kafka)
docker compose up
```

### 6) Testing
```bash
# Run all tests
make test

# Run with coverage
pytest --cov=. --cov-report=term --cov-report=html

# Run specific test file
pytest test/test_app.py -v

# Run with verbose output
pytest -v
```

Coverage reports are generated in:
- Terminal output
- `htmlcov/` directory (open `htmlcov/index.html` in browser)

## 📋 Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `KAFKA_BOOTSTRAP_SERVERS` | Yes | - | Kafka broker addresses (comma-separated) |
| `KAFKA_CONSUMER_GROUP` | Yes | - | Consumer group ID for Kafka |
| `KAFKA_TOPIC_NAME` | Yes | - | Topic to consume cocktail updates from |
| `LOG_LEVEL` | No | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |

### Pydantic Settings

Configuration is managed via `app_settings.py` using Pydantic BaseSettings:
- Type-safe configuration with validation
- Automatic environment variable loading
- Support for `.env` files
- Field aliases for flexible naming

## 🐳 Docker

### Build Image
```bash
# Development build
docker build -t data-extraction-agent .

# CI/CD build (used by pipeline)
docker build -f Dockerfile-CI -t data-extraction-agent:ci .
```

### Run Container
```bash
docker run --rm \
  -e KAFKA_BOOTSTRAP_SERVERS=kafka:9092 \
  -e KAFKA_CONSUMER_GROUP=extraction-group \
  -e KAFKA_TOPIC_NAME=cocktails-topic \
  data-extraction-agent
```

### Docker Compose
```bash
# Start all services (app + Kafka)
docker compose up

# Start in background
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

## 🧪 Testing

### Test Structure
- **Unit Tests**: Test individual components in isolation
- **Fixtures**: pytest fixtures for setup/teardown
- **Mocking**: pytest-mock for external dependencies
- **Coverage**: Minimum 80% code coverage target

### Test Commands
```bash
# Run all tests
make test

# Run with coverage report
pytest --cov=. --cov-report=term-missing

# Run specific test class
pytest test/test_app.py::TestSignalHandler -v

# Run with markers (if defined)
pytest -m unit
```

### Writing Tests
- Follow AAA pattern (Arrange, Act, Assert)
- Use descriptive test names
- Mock external dependencies (Kafka, APIs)
- Test both success and error paths
- Include type annotations

## 📦 Build & Deployment

### Local Build
```bash
# Run tests
make test

# Build Docker image
make docker-build

# Run linter
ruff check .

# Format code
ruff format .
```

### CI/CD Pipeline
GitHub Actions workflow (`.github/workflows/cezzis-rag-data-extraction-cicd.yaml`):

1. **GitVersion**: Semantic versioning
2. **Build**: Install dependencies, run tests, lint code
3. **Docker**: Build and push container image to ACR
4. **Release**: Create GitHub release on main branch

Artifacts:
- Test results and coverage reports
- Docker image: `acrveceusgloshared001.azurecr.io/cocktailsragdataextractionagent`
- GitHub release with semantic version

## 🔍 Code Quality

### Linting & Formatting
```bash
# Check formatting
ruff format --check .

# Format code
ruff format .

# Lint code
ruff check .

# Auto-fix issues
ruff check --fix .
```

### Configuration
- `.ruff.toml`: Ruff configuration
- `pytest.ini`: pytest settings
- `.dockerignore`: Docker build exclusions

### Pre-commit Checklist
- ✅ All tests pass
- ✅ Code formatted with ruff
- ✅ No linting errors
- ✅ Type hints added
- ✅ Documentation updated

## 🔒 Security Features

- **Environment Variables**: Secrets managed via env vars, never committed
- **Azure Key Vault**: Production secrets stored in Key Vault
- **Non-root User**: Container runs as non-root user for security
- **Input Validation**: Pydantic validates all configuration
- **Signal Handling**: Graceful shutdown with cleanup

## 📈 Monitoring & Observability

### Logging
- Structured logging to stdout
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Contextual information in log messages
- Errors include stack traces

### Future Enhancements
- OpenTelemetry integration for distributed tracing
- Metrics collection (messages processed, errors, latency)
- Health check endpoints
- Prometheus metrics export

## 🔄 Message Processing

### Kafka Consumer Behavior
- **Consumer Group**: Allows parallel processing
- **Auto Offset Reset**: `earliest` - processes from beginning on first run
- **Graceful Shutdown**: Commits offsets on SIGTERM/SIGINT
- **Error Handling**: Logs errors but continues processing

### Message Format
Expected message structure (JSON):
```json
{
  "cocktailId": "string",
  "action": "create|update|delete",
  "timestamp": "ISO8601",
  "data": {
    "name": "string",
    "ingredients": [...],
    "instructions": "string",
    ...
  }
}
```

## 🚧 Roadmap

- [ ] OpenTelemetry integration for observability
- [ ] Message schema validation with Pydantic models
- [ ] Dead letter queue for failed messages
- [ ] Metrics dashboard (Grafana)
- [ ] Integration tests with test containers
- [ ] Connection to vector storage service
- [ ] Batch processing optimization
- [ ] Retry logic with exponential backoff

## 🌐 Community & Support

- 🤝 **Contributing Guide** – see [CONTRIBUTING.md](../../.github/CONTRIBUTING.md)
- 🤗 **Code of Conduct** – see [CODE_OF_CONDUCT.md](../../.github/CODE_OF_CONDUCT.md)
- 🆘 **Support Guide** – see [SUPPORT.md](../../.github/SUPPORT.md)
- 🔒 **Security Policy** – see [SECURITY.md](../../.github/SECURITY.md)

## 📄 License

This project is proprietary software. All rights reserved. See [LICENSE](../../LICENSE) for details.

---

**Part of the Cezzis.com Cocktails ecosystem – Empowering cocktail discovery through AI and semantic search 🍸**
