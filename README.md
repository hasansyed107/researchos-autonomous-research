<p align="center">

<img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python" />
<img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi" />
<img src="https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react" />
<img src="https://img.shields.io/badge/LangGraph-Multi--Agent-orange?style=for-the-badge" />
<img src="https://img.shields.io/badge/Cerebras-Inference-red?style=for-the-badge" />
<img src="https://img.shields.io/badge/OpenRouter-LLM-purple?style=for-the-badge" />
<img src="https://img.shields.io/badge/Tavily-Search-success?style=for-the-badge" />
<img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />

</p>

<h1 align="center">ResearchOS</h1>

<h3 align="center">
Autonomous Research Intelligence Platform
</h3>

<p align="center">
Transform a single research query or PDF into an executive-grade research report using a fully autonomous 7-agent AI workflow powered by LangGraph, FastAPI, React, Cerebras, OpenRouter, and Retrieval-Augmented Generation (RAG).
</p>

<p align="center">

<a href="#installation">Quick Start</a> •
<a href="#features">Features</a> •
<a href="#architecture">Architecture</a> •
<a href="#installation">Installation</a> •
<a href="#deployment">Deployment</a>

</p>

---

# ResearchOS

ResearchOS is a **multi-agent autonomous research platform** that performs structured market intelligence, technology analysis, trend discovery, fact verification, and executive report generation.

Instead of relying on a single LLM response, ResearchOS coordinates multiple specialized AI agents that independently research, validate, review, and synthesize information into a professional, evidence-backed report.

The platform is designed for:

- Researchers
- Business Analysts
- Consultants
- Investors
- Product Managers
- Founders
- Enterprise Strategy Teams
- Students conducting technical research

ResearchOS combines autonomous reasoning, Retrieval-Augmented Generation (RAG), live web research, PDF grounding, and multi-model inference to produce high-quality reports with significantly greater transparency than a traditional chatbot.

---

# Screenshots

> **Replace these placeholders with screenshots from your application.**

## Dashboard

![Dashboard](docs/images/dashboard.png)

---

## Multi-Agent Workflow

![Workflow](docs/images/workflow.png)

---

## Generated Research Report

![Report](docs/images/report.png)

---

## PDF Export

![PDF Export](docs/images/pdf-export.png)

---

# Table of Contents

- [ResearchOS](#researchos)
- [Features](#features)
- [Multi-Agent Workflow](#multi-agent-workflow)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Research Pipeline](#research-pipeline)
- [Generated Reports](#generated-reports)
- [Deployment](#deployment)
- [CI/CD](#cicd)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

# Features

ResearchOS provides an end-to-end autonomous research workflow capable of transforming raw research questions into structured executive reports.

## Core Features

- Autonomous 7-Agent Research Workflow
- AI-Powered Research Planning
- Market Intelligence Analysis
- Technology Landscape Analysis
- Future Trend Discovery
- Fact Verification Layer
- Executive Report Generation
- Professional Markdown Reports
- PDF Report Export
- Live Workflow Progress Tracking
- Research Session History
- Token-Optimized Multi-Agent Pipeline

---

## AI Capabilities

- Multi-Agent Orchestration using LangGraph
- Retrieval-Augmented Generation (RAG)
- PDF Grounding
- Web Search Integration
- Source-backed Evidence Collection
- Multi-Model LLM Routing
- Automatic Retry & Fallback Handling
- Executive-Level Report Writing

---

## Report Output

Each report contains professionally structured sections including:

- Executive Summary
- Key Findings
- Market Analysis
- Technology Analysis
- Future Trends
- Strategic Recommendations
- Risk Assessment
- Source Coverage
- Retrieved PDF Evidence

---

## Why ResearchOS?

| Traditional AI Chatbots | ResearchOS |
|--------------------------|------------|
| Single LLM response | Multi-Agent reasoning |
| Limited verification | Fact-checking layer |
| Hallucination-prone | Source-grounded evidence |
| Generic summaries | Executive-grade reports |
| No workflow visibility | Live agent pipeline |
| Minimal context | Web + PDF + RAG integration |
| One-shot prompting | Structured autonomous research |

---

> **ResearchOS doesn't just answer questions—it conducts autonomous research.**


# Multi-Agent Workflow

ResearchOS follows a structured **7-agent autonomous research workflow** where each AI agent is responsible for a specific stage of the research lifecycle.

Unlike traditional chatbots, every stage is isolated, validated, and passed to the next agent through a shared LangGraph state.

text
                    User Research Query
                             │
                             ▼
                   ┌──────────────────┐
                   │  Planner Agent   │
                   └────────┬─────────┘
                            │
                            ▼
               ┌─────────────────────────┐
               │ Market Research Agent   │
               └────────┬────────────────┘
                        │
                        ▼
             ┌───────────────────────────┐
             │ Technology Research Agent │
             └────────┬──────────────────┘
                      │
                      ▼
              ┌─────────────────────────┐
              │ Future Trends Agent     │
              └────────┬────────────────┘
                       │
                       ▼
               ┌──────────────────────┐
               │ Reviewer Agent       │
               └────────┬─────────────┘
                        │
                        ▼
             ┌─────────────────────────┐
             │ Fact Checker Agent      │
             └────────┬────────────────┘
                      │
                      ▼
              ┌────────────────────────┐
              │ Writer Agent           │
              └────────┬───────────────┘
                       │
                       ▼
          Executive Research Report (Markdown + PDF)


---

# Agent Responsibilities

| Agent | Responsibility |
|--------|----------------|
| Planner | Breaks the research topic into a structured execution plan |
| Market Research | Collects market size, competitors, pricing, adoption signals, and commercial insights |
| Technology Research | Analyzes architecture, infrastructure, models, maturity, and technical limitations |
| Trends Research | Identifies emerging technologies, future adoption, and industry forecasts |
| Reviewer | Removes duplication, detects gaps, and improves report consistency |
| Fact Checker | Validates claims against collected evidence and retrieved documents |
| Writer | Produces the final executive-grade report in Markdown and PDF |

---

# System Architecture

ResearchOS is built using a modular microservice-style architecture that separates the user interface, orchestration engine, AI agents, retrieval pipeline, and language models.
text
                         ┌─────────────────────────────┐
                         │        React Frontend       │
                         │─────────────────────────────│
                         │ Dashboard                   │
                         │ Workflow Progress           │
                         │ Report Viewer               │
                         │ PDF Export                  │
                         └──────────────┬──────────────┘
                                        │
                                  HTTP / REST API
                                        │
                                        ▼
                         ┌─────────────────────────────┐
                         │      FastAPI Backend        │
                         │─────────────────────────────│
                         │ API Endpoints              │
                         │ PDF Upload                 │
                         │ Report Export              │
                         └──────────────┬──────────────┘
                                        │
                                        ▼
                         ┌─────────────────────────────┐
                         │    LangGraph Workflow       │
                         │─────────────────────────────│
                         │ Shared State               │
                         │ Agent Routing              │
                         │ Retry Logic                │
                         │ Error Recovery             │
                         └──────────────┬──────────────┘
                                        │
              ┌─────────────────────────┴─────────────────────────┐
              │                                                   │
              ▼                                                   ▼
     ┌────────────────────┐                           ┌────────────────────┐
     │  LLM Providers      │                           │ Retrieval Pipeline  │
     │────────────────────│                           │────────────────────│
     │ Cerebras           │                           │ Tavily Search      │
     │ OpenRouter         │                           │ PDF Processing     │
     │ Safe Fallback      │                           │ RAG               │
     └────────────────────┘                           └────────────────────┘
                                        │
                                        ▼
                          Executive Research Report


---

# Technology Stack

## Frontend

| Technology | Purpose |
|------------|---------|
| React 18 | User Interface |
| Vite | Development & Build Tool |
| Tailwind CSS | Styling |
| React Markdown | Report Rendering |
| Axios | API Communication |
| Lucide React | Icons |

---

## Backend

| Technology | Purpose |
|------------|---------|
| FastAPI | REST API |
| Python 3.11 | Backend Language |
| LangGraph | Multi-Agent Orchestration |
| LangChain | Agent Framework |
| PyMuPDF | PDF Processing |
| ReportLab | PDF Export |

---

## AI & Research

| Component | Purpose |
|-----------|---------|
| Cerebras | Primary LLM |
| OpenRouter | Fallback LLM |
| Tavily Search | Web Search |
| LangSmith | Workflow Tracing |
| Retrieval-Augmented Generation (RAG) | PDF Grounding |
| Multi-Agent Pipeline | Structured Research |

---

# Project Structure

text
ResearchOS/

├── backend/
│
│   ├── agents/
│   │   ├── planner.py
│   │   ├── market.py
│   │   ├── technology.py
│   │   ├── trends.py
│   │   ├── reviewer.py
│   │   ├── fact_checker.py
│   │   └── writer.py
│   │
│   ├── graph.py
│   ├── llm.py
│   ├── search.py
│   ├── rag.py
│   ├── pdf.py
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│
│   ├── src/
│   │
│   ├── components/
│   │
│   ├── pages/
│   │
│   ├── services/
│   │
│   ├── App.jsx
│   └── main.jsx
│
├── docs/
│   └── images/
│
├── README.md
├── LICENSE
└── .env.example

---

# Design Principles

ResearchOS is built around five core engineering principles.

- **Modularity** — Each AI agent performs a single responsibility.
- **Transparency** — Every report is grounded in collected evidence.
- **Reliability** — Automatic retry and deterministic fallbacks reduce failures.
- **Scalability** — New agents can be integrated without changing the workflow.
- **Extensibility** — Additional retrieval systems, LLM providers, or report templates can be added with minimal changes.

# Installation

ResearchOS can be installed either locally for development or deployed to a cloud environment.

---

## Prerequisites

Before installing ResearchOS, ensure the following software is installed:

| Requirement | Version |
|-------------|----------|
| Python | 3.11+ |
| Node.js | 20+ |
| npm | Latest |
| Git | Latest |

You will also need API keys for:

- Cerebras
- OpenRouter
- Tavily Search
- LangSmith (optional but recommended)

---

# Clone Repository

bash
git clone https://github.com/hasansyed107/ResearchOS.git

cd ResearchOS


---

# Backend Installation

Navigate to the backend directory.

`bash
cd backend


Create a virtual environment.

### Windows

`bash
python -m venv venv

venv\Scripts\activate
`

### Linux / macOS

`bash
python3 -m venv venv

source venv/bin/activate


Install dependencies.
``bash
pip install -r requirements.txt


---

# Frontend Installation

Open another terminal.

`bash
cd frontend


Install frontend dependencies.

bash
npm install


Start the development server.

`bash
npm run dev


The frontend will run at:

`
http://localhost:5173


---

# Start the Backend

Inside the backend folder run:

```bash
uvicorn main:app --reload
```

Backend API:

```
http://127.0.0.1:8000
```

Interactive API documentation:


http://127.0.0.1:8000/docs


---

# Environment Variables

Create a `.env` file inside the backend directory.

text
backend/
    .env


Example:

env
CEREBRAS_API_KEY=your_cerebras_api_key

OPENROUTER_API_KEY=your_openrouter_api_key

TAVILY_API_KEY=your_tavily_api_key

LANGSMITH_API_KEY=your_langsmith_api_key

LANGCHAIN_TRACING_V2=true

LANGCHAIN_PROJECT=ResearchOS


Never commit your `.env` file.

---

# Running ResearchOS

Start the backend.

`bash
uvicorn main:app --reload


Start the frontend.

bash


Open your browser.


http://localhost:5173


ResearchOS is now ready.

---

# Using ResearchOS

ResearchOS is designed around a simple research workflow.

### Step 1

Enter a research topic.

Examples:

- AI Coding Assistants
- Quantum Computing
- Semiconductor Industry
- EV Battery Market
- Robotics in Manufacturing
- Space Data Centers

---

### Step 2

(Optional)

Upload a PDF.

Supported documents include:

- Annual Reports
- Whitepapers
- Product Documentation
- Research Papers
- Internal Reports
- Investor Presentations

The uploaded document is indexed and used to ground the generated research.

---

### Step 3

Click




ResearchOS automatically launches the complete autonomous workflow.

---

### Step 4

Monitor live workflow progress.

Planner
↓

Market Research

↓

Technology Research

↓

Future Trends

↓

Reviewer

↓

Fact Checker

↓

Writer


Each stage updates independently.

---

### Step 5

Review the generated report.

Every report includes:

- Executive Summary
- Key Findings
- Market Analysis
- Technology Analysis
- Future Trends
- Strategic Recommendations
- Risks
- Source Coverage

---

### Step 6

Export the report.

ResearchOS supports:

- Markdown
- PDF

---

# Example Research Topics

## Artificial Intelligence

- AI Coding Assistants
- Agentic AI
- LLM Infrastructure
- AI Chips
- AI Data Centers
- AI in Healthcare
- AI in Finance

---

## Emerging Technologies

- Quantum Computing
- Edge Computing
- Robotics
- Autonomous Vehicles
- Battery Technology
- Semiconductor Manufacturing

---

## Market Research

- EV Battery Market
- Climate Technology
- Renewable Energy
- FinTech
- Cybersecurity
- Biotechnology

---

## Business Strategy

- Competitive Landscape
- Industry Analysis
- Technology Adoption
- Digital Transformation
- Market Entry Strategy
- Startup Research

---

# Generated Report Structure

Every report follows a consistent executive format.


Executive Summary

↓

Key Findings

↓

Market Analysis

↓

Technology Analysis

↓

Future Trends

↓

Strategic Recommendations

↓

Risk Assessment

↓

Conclusion

↓

Source Coverage


This standardized structure makes reports suitable for business reviews, technical analysis, consulting deliverables, and research documentation.

---

# Output Formats

ResearchOS currently supports:

| Format | Supported |
|----------|-----------|
| Markdown | ✅ |
| PDF | ✅ |
| Source-backed Report | ✅ |
| RAG Grounded Report | ✅ |
| Executive Summary | ✅ |

---

# Performance Features

ResearchOS is optimized for efficient multi-agent execution.

Highlights include:

- Token-efficient prompting
- Multi-model routing
- Automatic retry handling
- Deterministic fallback reports
- Source deduplication
- Research compression
- Markdown rendering
- PDF generation

# Multi-Agent Research Pipeline

ResearchOS is built around an autonomous multi-agent workflow where each agent specializes in one stage of the research lifecycle.

Instead of relying on a single prompt, every stage focuses on a dedicated task, resulting in higher-quality, source-grounded reports.

```
User Query / PDF
        │
        ▼
 Planner Agent
        │
        ▼
 Market Research Agent
        │
        ▼
 Technology Research Agent
        │
        ▼
 Trends Research Agent
        │
        ▼
 Reviewer Agent
        │
        ▼
 Fact Checker Agent
        │
        ▼
 Writer Agent
        │
        ▼
 Executive Research Report
```

---

# Planner Agent

The Planner Agent is responsible for understanding the user's objective and transforming it into a structured research strategy.

### Responsibilities

- Understand the research topic
- Define research objectives
- Break the problem into subtopics
- Guide downstream agents
- Improve research consistency

### Output

- Research plan
- Investigation goals
- Scope definition

---

# Market Research Agent

This agent investigates the commercial side of the topic.

### Responsibilities

- Market size
- CAGR
- Industry growth
- Competitors
- Commercial signals
- Pricing
- Funding
- Business landscape

### Data Sources

- Tavily Search
- Web reports
- Company websites
- Industry publications

### Output

- Market analysis
- Competitor insights
- Growth forecasts
- Business opportunities

---

# Technology Research Agent

Focuses entirely on technical intelligence.

### Responsibilities

- Architecture
- AI models
- Infrastructure
- Hardware
- Software stack
- Technical maturity
- Engineering challenges

### Output

- Technology analysis
- Infrastructure overview
- Technical comparison
- Engineering recommendations

---

# Trends Research Agent

Analyzes emerging technologies and future developments.

### Responsibilities

- Adoption trends
- Future forecasts
- Industry momentum
- Investment signals
- Innovation landscape

### Output

- Trend analysis
- Adoption outlook
- Future opportunities

---

# Reviewer Agent

Acts as the quality assurance layer.

### Responsibilities

- Detect missing information
- Remove duplicated findings
- Improve report consistency
- Identify weak arguments
- Improve report clarity

### Output

- Review notes
- Quality improvements
- Gap analysis

---

# Fact Checker Agent

Every important claim is validated before the final report.

### Responsibilities

- Validate statistics
- Verify market numbers
- Confirm company references
- Remove unsupported claims
- Flag inconsistencies

### Output

- Verified findings
- Fact validation report
- Confidence improvements

---

# Writer Agent

The Writer Agent synthesizes the outputs of all previous agents into a polished executive report.

### Responsibilities

- Merge research outputs
- Remove repetition
- Produce structured markdown
- Generate executive summaries
- Produce publication-ready reports

### Output

- Executive Report
- PDF-ready Markdown
- Structured findings

---

# LangGraph Workflow

ResearchOS uses **LangGraph** to orchestrate all agents.

LangGraph provides:

- Shared state management
- Sequential agent execution
- Error recovery
- Modular workflows
- Deterministic execution
`
State

↓

Planner

↓

Market

↓

Technology

↓

Trends

↓

Reviewer

↓

Fact Checker

↓

Writer

↓

Final Report


---

# Retrieval-Augmented Generation (RAG)

ResearchOS supports PDF-grounded research.

Users can upload documents to provide additional context for the research process.

Supported documents include:

- Annual Reports
- Whitepapers
- Research Papers
- Product Documentation
- Investor Presentations
- Internal Reports

---

## RAG Pipeline


Upload PDF

↓

PyMuPDF

↓

Text Extraction

↓

Chunking

↓

Embedding Generation

↓

Qdrant Vector Store

↓

Semantic Retrieval

↓

Relevant Context

↓

Research Agents


---

# Search Pipeline

ResearchOS combines web search with document retrieval.


User Query

↓

Planner

↓

Tavily Search

↓

Web Sources

↓

PDF Retrieval

↓

Merged Context

↓

Research Agents
`

This hybrid retrieval approach enables the system to combine public web knowledge with user-provided documents.

---

# Model Routing

ResearchOS uses a multi-model inference strategy for improved reliability.


Primary Model

↓

Cerebras

↓

Success?

↓

Yes → Continue

↓

No

↓

OpenRouter

↓

Continue Workflow


This fallback mechanism increases robustness and minimizes interruptions caused by provider outages or rate limits.

---

# Error Recovery

ResearchOS includes several safeguards to ensure reliable report generation.

### Automatic Retry

- API retries
- Network retry logic
- Timeout handling

### Safe Fallbacks

- Deterministic report generation
- Markdown cleanup
- Duplicate removal

### Validation

- Empty response detection
- Invalid markdown detection
- Source deduplication

These mechanisms ensure that users receive a usable report even when an upstream model or service fails.

---

# PDF Export

Generated reports can be exported as professionally formatted PDF documents.

Current export features include:

- Executive formatting
- Tables
- Markdown rendering
- Structured headings
- Source sections

This allows reports to be shared with stakeholders or included in business documentation.

---

# Continuous Integration & Continuous Deployment (CI/CD)

ResearchOS is designed to support automated testing and deployment using GitHub Actions.

Typical CI/CD workflow:


Developer Push

↓

GitHub

↓

GitHub Actions

↓

Install Dependencies

↓

Run Tests

↓

Build Frontend

↓

Build Backend

↓

Deploy
`

This enables reliable deployments with minimal manual intervention.

---

# Deployment Options

ResearchOS can be deployed using several modern platforms.

### Frontend

- Vercel
- Netlify

### Backend

- Railway
- Render
- Fly.io
- DigitalOcean

### Containers

- Docker
- Docker Compose

### Reverse Proxy

- Nginx

---

# Scalability

The architecture is modular and can be extended with additional agents or services.

Potential scaling strategies include:

- Parallel agent execution
- Redis caching
- Persistent vector databases
- Kubernetes deployment
- Background task queues
- Horizontal API scaling

ResearchOS is designed to evolve from a local research assistant into an enterprise-grade autonomous research platform.

# Example Research Topics

ResearchOS supports research across industries, technologies, markets, companies, and strategic initiatives.

### Artificial Intelligence

- AI Coding Assistants
- Agentic AI
- Large Language Models
- AI Infrastructure
- AI Safety
- Multimodal AI
- AI in Healthcare
- AI in Finance

### Technology

- Quantum Computing
- Robotics
- Autonomous Vehicles
- Computer Vision
- Cybersecurity
- Semiconductor Industry
- Edge Computing
- Cloud Computing

### Energy & Sustainability

- EV Battery Market
- Renewable Energy
- Hydrogen Economy
- Carbon Capture
- Nuclear Fusion
- Smart Grids

### Healthcare

- Digital Health
- Medical AI
- Biotechnology
- Drug Discovery
- Genomics
- Precision Medicine

### Business & Finance

- FinTech
- Digital Payments
- Venture Capital
- ESG Investing
- SaaS Market
- Supply Chain Technologies

---

# Example Report Structure

Every report generated by ResearchOS follows a consistent executive format.


Executive Summary

Key Findings

Market Analysis
    Market Snapshot
    Market Drivers
    Competitive Landscape
    Commercial Signals
    Market Challenges

Technology Analysis
    Current Technology
    Technology Comparison
    Current Capabilities
    Technical Challenges
    Infrastructure Requirements

Future Trends
    Emerging Trends
    Adoption Outlook

Strategic Recommendations

Risk Assessment

Conclusion

Source Coverage


Each section is generated independently using validated evidence before being synthesized into the final report.

---

# API Overview

ResearchOS exposes a REST API built with FastAPI.

## Generate Research


POST /research


Request

`json
{
    "query": "AI Coding Assistants"
}


Response

`json
{
    "title": "...",
    "report": "...",
    "workflow": {...}
}


---

## Export Report

`
POST /export-pdf


Exports the generated markdown report as a professionally formatted PDF.

---

## Health Check


GET /health


Returns service status for deployment monitoring.

---

# Performance Optimizations

ResearchOS includes several optimizations to reduce latency and improve reliability.

### Token Optimization

- Context compression
- Duplicate removal
- Source trimming
- Prompt optimization

### Retrieval Optimization

- Top-K semantic retrieval
- Source deduplication
- Context ranking
- PDF chunk filtering

### Reliability

- Automatic retries
- Multi-model fallback
- Safe markdown generation
- Deterministic fallback reports

---

# Current Limitations

Although ResearchOS is designed for production-ready research, there are several known limitations.

- Depends on external LLM providers
- Search quality depends on web availability
- PDF extraction quality varies with document formatting
- Very large documents may require chunking
- Market reports may contain conflicting estimates across sources

These limitations are mitigated through validation, source grounding, and fallback mechanisms.

---

# Future Roadmap

The long-term vision for ResearchOS is to evolve into a comprehensive autonomous research platform.

## Planned Features

### Research

- [ ] Multi-document research
- [ ] Cross-document reasoning
- [ ] Automatic citation generation
- [ ] Knowledge graph generation
- [ ] Interactive report refinement

### AI

- [ ] Multi-modal research
- [ ] Image understanding
- [ ] Audio and video analysis
- [ ] Agent memory
- [ ] Human-in-the-loop review

### Platform

- [ ] User authentication
- [ ] Team workspaces
- [ ] Project management
- [ ] Report versioning
- [ ] Research history search

### Infrastructure

- [ ] Redis caching
- [ ] Streaming responses
- [ ] Kubernetes deployment
- [ ] Horizontal scaling
- [ ] Enterprise monitoring

---

# Contributing

Contributions are welcome.

If you would like to improve ResearchOS:

1. Fork the repository.
2. Create a feature branch.
3. Implement your changes.
4. Add or update tests.
5. Submit a Pull Request.

Please follow the existing project structure and coding standards.

---

# Author

## Syed Ahmed Mubasirudin

**AI Engineer • Multi-Agent Systems • Retrieval-Augmented Generation • LangGraph**

Research interests include:

- Autonomous AI Agents
- Multi-Agent Systems
- Retrieval-Augmented Generation (RAG)
- LLM Infrastructure
- AI Product Engineering
- Intelligent Search Systems

### Connect

**GitHub**

https://github.com/hasansyed107

**LinkedIn**

https://linkedin.com/in/syed-ahmed-mubasirudin-28834b31b

**Email**

hasansyed004@gmail.com

---

# License

MIT License

Copyright (c) 2026 Syed Ahmed Mubasirudin

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies.

See the LICENSE file for the complete license text.

---

# Acknowledgements

ResearchOS is built using a modern open-source AI ecosystem.

Core technologies include:

- FastAPI
- React
- Tailwind CSS
- LangGraph
- LangChain
- Cerebras Inference
- OpenRouter
- Tavily Search
- Qdrant
- PyMuPDF
- ReportLab
- LangSmith

Their tools and communities make autonomous AI applications like ResearchOS possible.

---

# Star the Project

If you found ResearchOS useful, consider giving the repository a ⭐ on GitHub.

Your support helps improve the project and encourages future development.

---

<p align="center">

**ResearchOS**

*Autonomous Multi-Agent Research Intelligence Platform*

Built with ❤️ using React, FastAPI, LangGraph, Cerebras, OpenRouter, Tavily, Qdrant, PyMuPDF, and LangSmith.

</p>
