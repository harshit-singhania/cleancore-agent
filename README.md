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

### Quick Start (Using Dev Script)

The easiest way to get started is using the provided development script:

```bash
# Clone and enter the repository
git clone git@github.com:harshit-singhania/cleancore-agent.git
cd cleancore-agent

# First time setup - install dependencies
cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
cd ../frontend && npm install
cd ..

# Start both backend and frontend
./dev.sh start

# View status
./dev.sh status

# View logs
./dev.sh logs

# Stop all servers
./dev.sh stop
```

### Dev Script Commands

```bash
./dev.sh start                 # Start both servers
./dev.sh start --backend-only  # Start only backend
./dev.sh start --frontend-only # Start only frontend
./dev.sh stop                  # Stop all servers
./dev.sh restart               # Restart all servers
./dev.sh status                # Show server status
./dev.sh logs                  # Show recent logs
./dev.sh logs -n 100           # Show last 100 log lines
./dev.sh follow                # Follow logs in real-time
./dev.sh follow --backend-only # Follow backend logs only
./dev.sh open                  # Open frontend in browser
./dev.sh clean                 # Clean up logs and PID files
./dev.sh help                  # Show help
```

### Manual Setup (Alternative)

If you prefer to run servers manually:

**1. Setup the Translation Engine (FastAPI)**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend API will be available at: http://localhost:8000  
Interactive API docs: http://localhost:8000/docs

**2. Setup the Developer UI (React)**

```bash
cd frontend
npm install
npm run dev
```

Frontend app will be available at: http://localhost:5173

## 📁 Project Structure

```
cleancore-agent/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── requirements.txt     # Python dependencies
│   ├── venv/                # Python virtual environment
│   ├── routers/             # API route handlers
│   ├── services/            # Business logic services
│   ├── prompts/             # LLM prompt templates
│   └── models/              # Pydantic schemas
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main application component
│   │   ├── App.css          # Application styles
│   │   └── ...
│   ├── package.json         # Node dependencies
│   └── vite.config.js       # Vite configuration
├── dev.sh                   # Development server manager
└── README.md
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info and health check |
| `/health` | GET | Health status |
| `/api/v1/translate-abap` | POST | Translate legacy ABAP to Clean Core |

### Example API Usage

```bash
# Translate ABAP code
curl -X POST http://localhost:8000/api/v1/translate-abap \
  -H "Content-Type: application/json" \
  -d '{
    "code": "REPORT ZTEST.\nDATA: lv_val TYPE string."
  }'
```

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.11+, FastAPI, Uvicorn |
| LLM | Google GenAI SDK (Gemini 1.5 Flash) |
| Frontend | React 18+, Vite, react-diff-viewer |
| Styling | Tailwind CSS |

## 🔒 Security

- Zero-retention policy for proprietary enterprise code
- No ABAP code is persisted to disk or database
- In-memory processing only
- CORS restricted to local development origins

## 📝 License

Business Source License 1.1 (BSL 1.1)

## 🤝 Contributing

Please read [AGENTS.md](./AGENTS.md) for architectural guidelines before contributing.
