
# Cezzis.com Cocktails RAG Agent

> Part of the broader Cezzis.com digital experience for discovering and sharing cocktail recipes through AI-powered semantic search and retrieval-augmented generation.

[![CI](https://github.com/mtnvencenzo/cezzis-com-cocktails-rag-agent/actions/workflows/cezzis-rag-data-extraction-cicd.yaml/badge.svg?branch=main)](https://github.com/mtnvencenzo/cezzis-com-cocktails-rag-agent/actions/workflows/cezzis-rag-data-extraction-cicd.yaml)
[![Release](https://img.shields.io/github/v/release/mtnvencenzo/cezzis-com-cocktails-rag-agent?include_prereleases)](https://github.com/mtnvencenzo/cezzis-com-cocktails-rag-agent/releases)
[![License](https://img.shields.io/badge/license-Proprietary-lightgrey)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)
[![Last commit](https://img.shields.io/github/last-commit/mtnvencenzo/cezzis-com-cocktails-rag-agent?branch=main)](https://github.com/mtnvencenzo/cezzis-com-cocktails-rag-agent/commits/main)
[![Issues](https://img.shields.io/github/issues/mtnvencenzo/cezzis-com-cocktails-rag-agent)](https://github.com/mtnvencenzo/cezzis-com-cocktails-rag-agent/issues)
[![Project](https://img.shields.io/badge/project-Cezzis.com%20Cocktails-181717?logo=github&logoColor=white)](https://github.com/users/mtnvencenzo/projects/2)
[![Website](https://img.shields.io/badge/website-cezzis.com-2ea44f?logo=google-chrome&logoColor=white)](https://www.cezzis.com)

**End-to-end Retrieval-Augmented Generation (RAG) solution for semantic search and AI-powered cocktail discovery on [cezzis.com](https://cezzis.com).**

## 📖 Overview

This repository contains multiple interconnected services that work together to provide advanced semantic search and conversational AI capabilities for cocktail discovery. The solution processes real-time cocktail updates, generates vector embeddings, and enables natural language queries over the entire cocktail database.

## 🏗️ Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  Cocktails API  │─────▶│  Kafka/EventHub  │─────▶│ Data Extraction │
│                 │      │  (cocktails-topic)│      │     Agent       │
└─────────────────┘      └──────────────────┘      └────────┬────────┘
                                                              │
                                                              ▼
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   AI Services   │◀─────│  Vector Storage  │◀─────│   Embedding     │
│  (Ollama/TEI)   │      │    (Qdrant)      │      │    Pipeline     │
└─────────────────┘      └──────────────────┘      └─────────────────┘
         │                        │
         ▼                        ▼
┌─────────────────────────────────────────┐
│     RAG Query Orchestrator (Future)     │
│  Semantic Search & Conversational Q&A   │
└─────────────────────────────────────────┘
```

## 🧩 Applications

### Data Ingestion

#### 📥 [Data Extraction Agent](./data-ingestion/data-extraction-agent)
**Status:** ✅ Active Development

A Kafka consumer that processes cocktail data updates in real-time:
- Consumes messages from Kafka topics
- Extracts and validates cocktail data
- Prepares data for vectorization
- Handles graceful shutdown and offset management

**Tech Stack:** Python 3.12, Kafka (confluent-kafka), Pydantic, pytest

**[View Documentation →](./data-ingestion/data-extraction-agent/README.md)**

### Vector Storage & Embeddings *(Coming Soon)*

#### 🔢 Embedding Pipeline
**Status:** 🚧 Planned

Generates high-quality vector embeddings for cocktail data:
- Integrates with TEI (Text Embeddings Inference)
- Uses BAAI/bge-m3 model for advanced embeddings
- Processes cocktail names, ingredients, descriptions
- Stores vectors in Qdrant

#### 💾 Vector Storage Service
**Status:** 🚧 Planned

Manages vector database operations:
- Qdrant vector database integration
- Similarity search capabilities
- Vector indexing and updates
- Query optimization

### Query & Retrieval *(Coming Soon)*

#### 🔍 Query Processor
**Status:** 🚧 Planned

Handles semantic search queries:
- Natural language query processing
- Vector similarity search
- Result ranking and filtering
- Context retrieval for RAG

#### 🤖 RAG Orchestrator
**Status:** 🚧 Planned

Coordinates retrieval and generation:
- Integrates with Ollama for LLM inference
- Combines retrieved context with user queries
- Generates conversational responses
- REST API for semantic search and Q&A

## 🧩 Cezzis.com Project Ecosystem

This RAG solution works alongside several sibling repositories:

- **cocktails-rag-agent** (this repo) – RAG solution for semantic search and AI-powered discovery
- [**cocktails-mcp**](https://github.com/mtnvencenzo/cezzis-com-cocktails-mcp) – Model Context Protocol server for AI agents
- [**cocktails-api**](https://github.com/mtnvencenzo/cezzis-com-cocktails-api) – ASP.NET Core backend and REST API
- [**cocktails-web**](https://github.com/mtnvencenzo/cezzis-com-cocktails-web) – React SPA for the public experience
- [**cocktails-common**](https://github.com/mtnvencenzo/cezzis-com-cocktails-common) – Shared libraries and utilities
- [**shared-infrastructure**](https://github.com/mtnvencenzo/shared-infrastructure) – Global Terraform modules

## ☁️ Cloud Infrastructure (Azure)

Infrastructure is provisioned with Terraform and deployed into Azure:

- **Azure Container Apps** – Hosts all microservices with auto-scaling
- **Azure Event Hubs / Kafka** – Event streaming for real-time data ingestion
- **Azure Container Registry** – Stores container images
- **Azure Key Vault** – Manages secrets and credentials
- **Azure Monitor** – Telemetry and observability via OpenTelemetry
- **Azure AI Search** *(planned)* – Alternative/complement to Qdrant for vector search

## ✨ Features

### Current (Data Extraction Agent)
- ✅ **Real-time Data Ingestion:** Kafka consumer for cocktail updates
- ✅ **Type-safe Configuration:** Pydantic-based settings with validation
- ✅ **Graceful Shutdown:** Proper signal handling and cleanup
- ✅ **Comprehensive Testing:** Unit tests with pytest and pytest-mock
- ✅ **CI/CD Pipeline:** Automated build, test, and deployment
- ✅ **Container Ready:** Docker and Kubernetes deployment

### Planned
- 🚧 **Semantic Search:** Vector similarity search for cocktails
- 🚧 **Conversational Q&A:** Natural language queries with LLM responses
- 🚧 **Advanced Embeddings:** BAAI/bge-m3 via TEI for high-quality vectors
- 🚧 **RAG Pipeline:** Full retrieval-augmented generation workflow
- 🚧 **API Gateway:** REST API for search and conversational interfaces
- 🚧 **Monitoring Dashboard:** Real-time metrics and observability

## 🛠️ Tech Stack

### Data Ingestion
- **Python 3.12+** – Modern Python with type hints
- **Apache Kafka** – Event streaming via confluent-kafka
- **Pydantic** – Configuration and data validation

### Vector & Embeddings (Planned)
- **Qdrant** – Vector database for similarity search
- **TEI (Text Embeddings Inference)** – Embedding service
- **BAAI/bge-m3** – State-of-the-art multilingual embeddings

### AI & Generation (Planned)
- **Ollama** – Local LLM inference
- **RAG Framework** – Custom retrieval-augmented generation

### Infrastructure
- **Azure Container Apps** – Serverless containers
- **Azure Event Hubs** – Managed Kafka
- **Azure Key Vault** – Secrets management
- **Terraform** – Infrastructure as Code
- **GitHub Actions** – CI/CD automation

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Docker and Docker Compose
- Make (build automation)
- Azure CLI (for cloud deployment)

### Quick Start - Data Extraction Agent

1. **Clone the repository**
   ```bash
   git clone https://github.com/mtnvencenzo/cezzis-com-cocktails-rag-agent.git
   cd cezzis-com-cocktails-rag-agent/data-ingestion/data-extraction-agent
   ```

2. **Set up virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Configure environment**
   ```bash
   # Create .env file
   cat > .env << EOF
   KAFKA_BOOTSTRAP_SERVERS=localhost:9092
   KAFKA_CONSUMER_GROUP=extraction-group
   KAFKA_TOPIC_NAME=cocktails-topic
   EOF
   ```

5. **Run tests**
   ```bash
   make test
   ```

6. **Start the application**
   ```bash
   python src/app.py
   ```

For detailed setup and configuration, see the [Data Extraction Agent documentation](./data-ingestion/data-extraction-agent/README.md).

### Docker Compose (Full Stack - Coming Soon)

```bash
# Start all services
docker compose up

# This will include:
# - Kafka/Zookeeper
# - Data Extraction Agent
# - Qdrant Vector DB
# - TEI Embedding Service
# - Ollama LLM Service
```

## � Repository Structure

```text
cezzis-com-cocktails-rag-agent/
├── data-ingestion/
│   └── data-extraction-agent/     # ✅ Kafka consumer (Active)
│       ├── src/
│       ├── test/
│       ├── Dockerfile
│       └── README.md
├── vector-storage/                # 🚧 Vector DB service (Planned)
├── embedding-pipeline/            # 🚧 TEI integration (Planned)
├── query-processor/               # 🚧 Search service (Planned)
├── rag-orchestrator/              # 🚧 RAG coordinator (Planned)
├── terraform/                     # Infrastructure as Code
├── .github/                       # CI/CD workflows and templates
│   ├── workflows/
│   │   └── cezzis-rag-data-extraction-cicd.yaml
│   ├── CODE_OF_CONDUCT.md
│   ├── CONTRIBUTING.md
│   ├── SECURITY.md
│   └── SUPPORT.md
├── docker-compose.yml             # Local development stack
├── LICENSE
└── README.md                      # This file
```

## 🧪 Testing

Each application includes comprehensive tests:

```bash
# Data Extraction Agent
cd data-ingestion/data-extraction-agent
make test

# Run with coverage
pytest --cov=. --cov-report=term --cov-report=html

# Future: Vector Storage tests
cd vector-storage
pytest
```

## 📦 CI/CD

GitHub Actions workflows automate:

- **Build & Test**: Run tests, linting, and code quality checks
- **Docker**: Build and push container images to ACR
- **Release**: Semantic versioning and GitHub releases
- **Deploy**: Deploy to Azure Container Apps (future)

See [`.github/workflows/`](./.github/workflows/) for pipeline definitions.

## 🗺️ Roadmap

### Phase 1: Data Ingestion ✅ (Current)
- [x] Kafka consumer implementation
- [x] Configuration management with Pydantic
- [x] Unit tests with pytest
- [x] CI/CD pipeline
- [x] Docker containerization
- [x] Documentation

### Phase 2: Vector Storage 🚧 (Next)
- [ ] Qdrant integration
- [ ] TEI embedding service
- [ ] BAAI/bge-m3 model deployment
- [ ] Embedding pipeline
- [ ] Vector indexing and updates
- [ ] Similarity search API

### Phase 3: Query & Retrieval 🚧
- [ ] Query processor service
- [ ] Semantic search implementation
- [ ] Result ranking and filtering
- [ ] Context retrieval for RAG
- [ ] API gateway

### Phase 4: RAG Orchestration 🚧
- [ ] Ollama integration
- [ ] RAG pipeline implementation
- [ ] Conversational Q&A API
- [ ] Response streaming
- [ ] Prompt engineering and optimization

### Phase 5: Production Readiness 🚧
- [ ] OpenTelemetry integration
- [ ] Monitoring dashboards
- [ ] Performance optimization
- [ ] Load testing
- [ ] Azure deployment automation
- [ ] API documentation

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

- 📖 **[Contributing Guide](./.github/CONTRIBUTING.md)** - How to contribute
- 🤗 **[Code of Conduct](./.github/CODE_OF_CONDUCT.md)** - Community guidelines
- 🆘 **[Support Guide](./.github/SUPPORT.md)** - Getting help
- 🔒 **[Security Policy](./.github/SECURITY.md)** - Security reporting

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`make test`)
5. Commit your changes (`git commit -m 'feat: add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📊 Project Status

- 🚀 **Status**: Active Development
- 🎯 **Current Focus**: Data Ingestion Pipeline
- 👤 **Maintainer**: [@mtnvencenzo](https://github.com/mtnvencenzo)
- 📈 **Roadmap**: See [Issues](https://github.com/mtnvencenzo/cezzis-com-cocktails-rag-agent/issues) and [Projects](https://github.com/mtnvencenzo/cezzis-com-cocktails-rag-agent/projects)

## 🌐 Resources

- 🌍 **Website**: [cezzis.com](https://www.cezzis.com)
- 📚 **API Docs**: [api.cezzis.com](https://api.cezzis.com)
- 🤖 **MCP Server**: [cocktails-mcp](https://github.com/mtnvencenzo/cezzis-com-cocktails-mcp)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/mtnvencenzo/cezzis-com-cocktails-rag-agent/discussions)
- 🐛 **Issues**: [GitHub Issues](https://github.com/mtnvencenzo/cezzis-com-cocktails-rag-agent/issues)

## 📄 License

This project is proprietary software. All rights reserved. See [LICENSE](LICENSE) for details.

---

**Part of the Cezzis.com Cocktails ecosystem – Empowering cocktail discovery through AI and semantic search 🍸**