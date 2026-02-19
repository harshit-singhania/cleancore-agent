# AGENTS.md — CleanCore Agent

> **Purpose:** This document provides essential context for AI coding assistants working on the CleanCore Agent codebase. Read this entire file before proposing any code changes.

---

## 🎯 Project Mission

CleanCore Agent is an AI-powered SAP ABAP modernization tool. It translates legacy custom ABAP code into S/4HANA Clean Core compliant code using Google's Gemini 1.5 Flash LLM.

**Core Value Proposition:**
- Transform legacy Z-programs, obsolete `SELECT` queries, and implicit enhancements into RAP-managed business objects
- Enforce SAP's A-D Extensibility Model (Level A = compliant, Level D = forbidden)
- Maintain zero-retention for proprietary enterprise code

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Backend | Python 3.11+, FastAPI | Translation API, LLM orchestration |
| LLM | Google GenAI SDK (Gemini 1.5 Flash) | Massive context window (1M+ tokens) for full module ingestion |
| Frontend | React 18+, Vite, `react-diff-viewer` | Side-by-side code diff UI |
| Styling | Tailwind CSS | Consistent enterprise UI |
| Dev Tools | Ruff (linting), Uvicorn (server) | Code quality & local dev |

**Environment:** Windows local development (use `venv\Scripts\activate`)

---

## 📜 Architectural Rules (NON-NEGOTIABLE)

### 1. Zero Hallucinated ABAP
Standard LLMs generate fictional SAP syntax. The `/api/v1/translate-abap` endpoint MUST:

- Use a **highly structured system prompt** that explicitly references:
  - ABAP Cloud (ABAP for Cloud Development)
  - RAP (RESTful Application Programming Model)
  - Released Public APIs only
  - CDS Views for data modeling
- **FORBID** Level D approaches in generated code:
  - Implicit enhancements
  - Direct table updates (`UPDATE ztable`)
  - Unreleased internal APIs
  - Modification of SAP standard code

**System Prompt Template Location:** `backend/prompts/abap_clean_core_v1.txt`

### 2. Stateless Translation Pipeline
Enterprise code is highly proprietary. The backend MUST:
- Process ABAP payloads **entirely in memory**
- NEVER write incoming code to disk or database
- Return translated payload immediately to frontend
- Log only metadata (timestamp, token count) — never code content

### 3. Dual-Pane Diff UI
The React frontend MUST maintain:
- **Left Pane:** Read-only, syntax-highlighted legacy ABAP input
- **Right Pane:** Read-only, syntax-highlighted S/4HANA compliant output
- **Visual Indicators:** Line-by-line diff highlighting (added/removed/changed)
- **Copy Actions:** One-click copy for translated code

### 4. Context Window Optimization
Gemini 1.5 Flash supports 1M+ tokens. Code chunking rules:
- **DO NOT chunk** unless input exceeds 900k tokens (safety margin)
- If chunking required, use semantic boundaries (CLASS/FORM/METHOD blocks)
- Preserve cross-reference context across chunks

### 5. Error Handling Standards
All API errors MUST return structured JSON:
```json
{
  "error": {
    "code": "INVALID_ABAP_SYNTAX",
    "message": "Parse error at line 47",
    "details": { "line": 47, "column": 12 }
  }
}
```

---

## 📁 Project Structure

```
cleancore-agent/
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── routers/
│   │   └── translate.py        # /api/v1/translate-abap endpoint
│   ├── services/
│   │   ├── gemini_client.py    # Google GenAI wrapper
│   │   └── abap_parser.py      # ABAP syntax validation
│   ├── prompts/
│   │   └── abap_clean_core_v1.txt  # System prompt template
│   └── models/
│       └── schemas.py          # Pydantic models
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CodeInput.tsx       # Left pane input
│   │   │   ├── CodeOutput.tsx      # Right pane output
│   │   │   └── DiffViewer.tsx      # Side-by-side diff
│   │   ├── services/
│   │   │   └── api.ts              # Backend client
│   │   └── App.tsx
│   └── index.html
└── AGENTS.md
```

---

## ⚡ Development Commands

```bash
# Backend
ruff check --fix .              # Lint & auto-fix Python
uvicorn main:app --reload       # Start dev server (http://localhost:8000)

# Frontend
npm run dev                     # Start Vite dev server (http://localhost:5173)
npm run build                   # Production build
npm run preview                 # Preview production build
```

---

## 🔒 Security & Compliance Checklist

Before submitting any code change, verify:

- [ ] No ABAP code is persisted to disk/database
- [ ] API keys (Gemini) are loaded from environment variables only
- [ ] CORS is restricted to local dev origins only
- [ ] No PII or proprietary code in logs
- [ ] Input validation prevents prompt injection

---

## 🧪 Testing Expectations

- **Backend:** Add pytest tests for new endpoints in `backend/tests/`
- **Frontend:** Add component tests for new UI elements in `frontend/src/components/__tests__/`
- **Integration:** Verify end-to-end flow with sample ABAP programs from `backend/tests/fixtures/`

---

## 🤖 LLM Interaction Guidelines

When modifying Gemini integration code:

1. **Temperature:** Use `temperature=0.1` for deterministic translation
2. **Max Tokens:** Set based on input size (output ≈ 1.2x input for commented code)
3. **Retry Logic:** Implement exponential backoff for 429/503 errors
4. **Response Parsing:** Always validate JSON structure before returning to frontend

---

## 📝 Code Style

- **Python:** Follow PEP 8, use type hints, docstrings in Google format
- **TypeScript:** Strict mode enabled, functional components with hooks
- **Naming:** `snake_case` for Python, `PascalCase` for components, `camelCase` for variables
