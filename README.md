# CleanCore Agent 🚀 ERP

**Automated SAP ABAP to S/4HANA Code Modernization using AI.**

CleanCore Agent is an enterprise-grade developer tool that automates the translation of legacy custom ABAP code into SAP's modern **RESTful Application Programming Model (RAP)**. By leveraging massive context-window LLMs, it turns a multi-year manual consulting nightmare into an instant software translation problem, ensuring strict compliance with S/4HANA Clean Core principles.

## 🚨 The Enterprise Problem
By 2027, every Fortune 500 company running SAP must migrate to S/4HANA. SAP has strictly enforced a new **A-D Extensibility Model**. Millions of lines of legacy custom code (Level D - non-compliant) must be manually rewritten to use released public APIs and ABAP Cloud (Level A - upgrade-safe). Boutique IT firms are drowning in the manual syntax rewrite process.

## 💡 The AI Solution
CleanCore Agent acts as a high-speed copilot for ABAP architects:
- **Massive Context Ingestion:** Powered by Gemini 1.5 Flash, the engine can ingest entire legacy SAP modules (custom Z-programs, obsolete `SELECT` queries) in a single pass.
- **Clean Core Enforcement:** Automatically flags SAP internal objects and refactors them into RAP-managed business objects and OData V4 services.
- **Dual-Pane Dashboard:** A sleek developer UI where consultants paste legacy code on the left and receive Cloud-ready ABAP on the right in seconds.

## 🏗️ Architecture MVP
- **Translation Engine:** Python / FastAPI backend interfacing with Gemini 1.5 Flash via a specialized RAG pipeline grounded in SAP documentation.
- **Developer UI:** React / Vite web dashboard with syntax-highlighted diffing.
- **Security:** Zero-retention policy for proprietary enterprise code.

## 💻 Local Developer Setup

**1. Clone the repository**
```bash
git clone git@github.com:yourusername/cleancore-agent.git
cd cleancore-agent
```

**2. Setup the Translation Engine (FastAPI)**

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

**3. Setup the Developer UI (React)**

```bash
cd frontend
npm install
npm run dev
```
