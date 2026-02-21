# CleanCore Agent 🚀 ERP

**Automated SAP ABAP to S/4HANA Code Modernization using AI.**

CleanCore Agent makes legacy system conversions (ABAP to ABAP Cloud/RAP) an instant AI-powered problem, enforcing compliance with S/4HANA Clean Core principles via high-precision RAG.

## 🚨 The Enterprise Problem

By 2027, every Fortune 500 company running SAP must migrate to S/4HANA. SAP has strictly enforced a new **A-D Extensibility Model**. Millions of lines of legacy custom code (Level D - non-compliant) must be manually rewritten to use released ABAP Cloud APIs.

## 💡 The AI Solution (CleanCore Agent)

- **Massive Context Ingestion:** Powered by Gemini 1.5.
- **RAG-Augmented Ground Truth:** Pulls from SAP documentation securely using Qdrant vector databases.
- **Enterprise Ready Data:** Stores full metadata for Projects, Users, Translation results via Supabase and Prisma.

## 🛠️ Current Tech Stack & Services

- **Backend Logic:** Python 3.11, FastAPI
- **Database / ORM:** PostgreSQL (via Supabase pooling), Prisma
- **Vector DB:** Qdrant (Local via Docker/Colima or Cloud)
- **AI Models:** Google GenAI SDK (`gemini-1.5-flash` / `text-embedding-004`)

## 💻 Local Developer Setup

### 1. Requirements

Ensure you have Python 3.11+, Node.js (for Prisma), and Colima/Docker installed.

### 2. Environment Variables

Create a `.env.local` based on the `.env` template to link your Supabase database and Gemini API Key.

### 3. Database & Prisma

```bash
npm install
npx prisma db push
npx prisma generate
```

### 4. Qdrant (Colima)

```bash
colima start
docker-compose up -d qdrant
# Verify on http://localhost:6333
```

### 5. Start Backend API

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m src.api.main
```

The API is available at `http://localhost:8080`.

## 📁 Project Structure

Please refer to [`AGENTS.md`](./AGENTS.md) at the root level (and inside subdirectories) for detailed architectural documentation used both manually and by agentic copilots.

## 📝 License

Business Source License 1.1 (BSL 1.1)
