
# 🍸 cezzis-com-cocktails-rag-agent

**End-to-end Retrieval-Augmented Generation (RAG) agent for [cezzis.com](https://cezzis.com) cocktails.**

> 🚧 **Work in Progress** 🚧  
> This project is under active development. Features and documentation may change frequently.

## 📖 Overview

This repository aims to build a modern RAG agent for cocktail data, leveraging:

- **Python** for backend logic
- **Qdrant** as the vector database
- **Ollama** for large language model (LLM) inference
- **Azure Cosmos DB** as the data source
- **TEI** with `BAAI/bge-m3` for advanced text embeddings

The agent provides a REST API for:

- Semantic search over cocktail recipes and metadata
- Conversational Q&A using state-of-the-art embeddings and LLMs

## ✨ Features

- **Semantic Search:** Find cocktails by ingredients, flavor profiles, and more using vector similarity.
- **Conversational Q&A:** Ask natural language questions about cocktails and get intelligent answers.
- **Advanced Embeddings:** Utilizes BAAI/bge-m3 for high-quality text representations.
- **Scalable Architecture:** Designed for extensibility and cloud deployment.

## 🛠️ Tech Stack

- Python
- Qdrant (Vector DB)
- Ollama (LLM)
- Azure Cosmos DB
- TEI + BAAI/bge-m3

## 🚀 Getting Started

> **Note:** The codebase is still being developed. Setup instructions and usage examples will be added soon.

## 🗺️ Roadmap

- [ ] Initial API scaffolding
- [ ] Integration with Qdrant and Cosmos DB
- [ ] Embedding pipeline with TEI and BAAI/bge-m3
- [ ] REST endpoints for search and Q&A
- [ ] Documentation and usage examples

## 📄 License

This project is licensed under a **proprietary license**. See the [LICENSE](LICENSE) file for details.