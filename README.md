# OSINT Fuzzy

> An AI-powered Open Source Intelligence platform for cybersecurity threat research and analysis.

## Overview

OSINT Fuzzy is an intelligent OSINT platform that combines **LLMs**, **Retrieval-Augmented Generation (RAG)**, and **autonomous agents** to automate cybersecurity intelligence workflows. It ingests data from multiple open sources, builds a searchable knowledge base, and provides natural language interfaces for threat research, vulnerability analysis, and security investigations.

## Key Features

- **Multi-Source Data Collection**: Automated ingestion from ArXiv (security papers), MITRE ATT&CK, NVD (CVE database), PDFs, and web sources
- **Semantic Knowledge Base**: Document chunking with security-aware context preservation and vector embeddings for semantic search
- **RAG Pipeline**: Grounded responses with source attribution by retrieving relevant context from the knowledge base
- **Autonomous Agents**: ReAct-style reasoning agents with specialized tools for entity extraction, relationship analysis, and timeline generation
- **Dual Interface**: Interactive Streamlit web UI and command-line interface with multi-turn conversation support

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Data Sources   │────▶│  Processing &    │────▶│  Knowledge Base │
│  (ArXiv, MITRE, │     │  Embedding       │     │  (Vectors +     │
│   NVD, PDFs)    │     │  Pipeline        │     │   Documents)    │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
┌─────────────────┐     ┌──────────────────┐              │
│  User Interface │◀────│  Query Router    │◀─────────────┘
│  (Streamlit/CLI)│     │  (RAG or Agent)  │
└─────────────────┘     └────────┬─────────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
           ┌─────────────────┐      ┌─────────────────┐
           │  RAG Pipeline   │      │  Agent Framework│
           │  (Context + LLM)│      │  (Tools + Loop) │
           └─────────────────┘      └─────────────────┘
```

## Tech Stack

| Category | Technologies |
|----------|--------------|
| **Language** | Python 3.10+ |
| **LLM** | Anthropic Claude 3.7 Sonnet |
| **Framework** | LangChain |
| **Embeddings** | Sentence Transformers (all-MiniLM-L6-v2) |
| **Vector Store** | File-based JSON (extensible to Milvus/pgvector) |
| **UI** | Streamlit, CLI (argparse) |
| **Data Processing** | unstructured, PyPDF2, BeautifulSoup, spaCy |

## Quick Start

### 1. Setup

```bash
# Clone and navigate
git clone <repository_url>
cd osint-fuzzy

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.template .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 2. Collect Data

```bash
python collect_arxiv.py    # Security research papers
python collect_mitre.py    # ATT&CK framework
python collect_nvd.py      # CVE database
```

### 3. Build Knowledge Base

```bash
python ingest_documents.py
```

### 4. Run the Application

**Web Interface:**
```bash
streamlit run app.py
```

**Command Line:**
```bash
python osint_cli.py
```

## Project Structure

```
osint-fuzzy/
├── src/
│   ├── agent/           # Autonomous agent framework
│   ├── chatbot/         # UI logic and query routing
│   ├── data_collection/ # Loaders and processors
│   ├── knowledge_base/  # Chunking, embeddings, storage
│   ├── llm/             # Claude API integration
│   ├── rag/             # RAG pipeline
│   └── utils/           # Helper utilities
├── collect_*.py         # Data collection scripts
├── ingest_documents.py  # KB population script
├── app.py               # Streamlit web UI
├── osint_cli.py         # CLI interface
└── requirements.txt     # Dependencies
```

## Example Queries

**RAG-driven (factual):**
- "What is CVE-2023-1234?"
- "Explain zero trust architecture"

**Agent-driven (analytical):**
- "Analyze APT29's attack methods"
- "Create a timeline of the SolarWinds incident"
- "Extract all CVEs and IPs from this report"

---

*Built as a demonstration of AI-driven OSINT capabilities for cybersecurity analysis.*
