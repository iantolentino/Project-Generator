# 🚀 Project Generator v2.0

> **Full-stack project scaffolding in seconds.**
> Pick your stack → generate → only edit `.env` → start building.

Supports **7 production-ready stacks** across Web, Desktop, and Hybrid platforms. Works as an interactive CLI **or** a self-hosted web app with a REST API you can `curl`.

---

## ✨ What's Generated

Every project comes with:

| What | Details |
|------|---------|
| **Full project structure** | All folders, files, and configs |
| **Auth system** | Login, register, JWT or sessions – wired and working |
| **Database layer** | Schema / models already defined |
| **Docker Compose** | One command to run everything with a DB GUI |
| **API routes** | RESTful endpoints with validation + error handling |
| **Environment file** | `.env.example` – just copy and fill in secrets |
| **README per project** | Stack-specific quick-start guide |

---

## 🛠 Supported Stacks

| Stack ID | Framework | Database | Auth | Use for |
|----------|-----------|----------|------|---------|
| `nextjs_postgres_prisma` | **Next.js 14** (App Router) | PostgreSQL | NextAuth | E-commerce, SaaS, Dashboards, Blogs |
| `react_node_mongo` | **React + Express** | MongoDB | JWT | Social apps, Streaming, Gaming |
| `django_postgres` | **Django REST** | PostgreSQL | SimpleJWT | Healthcare, LMS, Ticketing |
| `vue_express_mysql` | **Vue 3 + Express** | MySQL | JWT | Restaurants, Finance, Inventory |
| `react_static` | **React + Vite** | — | — | Portfolios, Landing pages |
| `electron_sqlite` | **Electron + React** | SQLite | — | Desktop apps |
| `tauri_react` | **Tauri + React** | SQLite | — | Lightweight desktop apps |

---

## ⚡ Quick Start

### Prerequisites

```bash
# Python 3.10+
python --version

# Install dependencies
pip install -r requirements.txt
```

---

## 🖥 Mode 1 – Interactive CLI

```bash
python main.py
```

Walk through 6 prompts and get a folder generated in your current directory.

```
╔══════════════════════════════════════════════════════╗
║          🚀  Project Generator  v2.0                 ║
╚══════════════════════════════════════════════════════╝

1️⃣  Select platform:        Web
2️⃣  Choose category:        E-commerce
   💡 Suggested: Next.js 14 + PostgreSQL + Prisma
3️⃣  Primary color:          #6366f1
4️⃣  Design style:           Modern
5️⃣  Project scope:          Scalable app
6️⃣  Project name:           my-shop

✅ Project ready!
   📁 /home/you/my-shop

🔑 Next steps:
   1. cd my-shop
   2. cp .env.example .env
   3. Fill in secret values  ← only thing you need to edit!
   4. npm install && npm run db:push && npm run db:seed && npm run dev
```

---

## 🌐 Mode 2 – Web UI + REST API

Start the server:
```bash
python main.py --web
# or
python main.py --web --port 8080
```

Open **http://localhost:5050** in your browser.

```
🌐  Project Generator Web UI  →  http://localhost:5050
   API: http://localhost:5050/api/generate
```

The web UI lets you:
- Select all options via a clean dark-mode interface
- Preview the resolved tech stack instantly
- Click **Generate & Download ZIP** – ready in < 1 second

---

## 📡 Mode 3 – REST API / cURL

Generate a project from any script, CI pipeline, or tool:

### Generate a ZIP

```bash
curl -X POST http://localhost:5050/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "shop-app",
    "platform":     "Web",
    "category":     "E-commerce",
    "colors":       ["#6366f1"],
    "style":        "Modern",
    "scope":        "Scalable app"
  }' \
  --output shop-app.zip
```

Then:
```bash
unzip shop-app.zip
cd shop-app
cp .env.example .env
# Fill in secrets, then:
npm install && npm run db:push && npm run dev
```

### List all stacks

```bash
curl http://localhost:5050/api/stacks | python -m json.tool
```

### Preview stack for options (no file generation)

```bash
curl -X POST http://localhost:5050/api/preview \
  -H "Content-Type: application/json" \
  -d '{"platform":"Web","category":"Social media app"}'
```

### API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/generate` | Generate project ZIP |
| `GET` | `/api/stacks` | List all stack metadata |
| `POST` | `/api/preview` | Preview resolved stack |

**POST `/api/generate` body:**
```json
{
  "project_name": "my-app",        // required
  "platform":     "Web",           // required: Web | Desktop | Hybrid
  "category":     "E-commerce",    // required: see list below
  "colors":       ["#6366f1"],     // optional: primary brand color
  "style":        "Modern",        // optional
  "scope":        "Scalable app"   // optional
}
```

**Response headers:**
```
X-Stack-Id:    nextjs_postgres_prisma
X-Stack-Label: Next.js 14 + PostgreSQL + Prisma
Content-Type:  application/zip
```

---

## 📋 Available Categories

```
Web:     E-commerce · SaaS product · Business dashboard · Blogging platform
         AI chatbot interface · Streaming platform · Social media app
         Video conferencing · Cryptocurrency tracker · Gaming hub
         Ticketing system · Learning management system · Healthcare management
         Event management · Travel booking · Restaurant ordering system
         Finance tracker · Inventory management · Portfolio site · Music player

Desktop: All categories → Electron + React + SQLite
Hybrid:  All categories → Tauri + React + SQLite
```

---

## 📁 Project Structure

```
Project-Generator/
├── main.py                   # Unified entry point (CLI or web)
├── requirements.txt
├── setup.py
├── structure.py              # Tkinter folder tree viewer (standalone)
└── project_gen/
    ├── __init__.py
    ├── cli.py                # Interactive terminal prompts
    ├── server.py             # Flask web server + REST API + UI
    ├── generator.py          # Disk writer (CLI) + ZIP builder (API)
    ├── stacks.py             # All 7 stack templates (full code)
    ├── prompts.py            # questionary CLI prompts
    └── utils.py              # Helpers
```

---

## 🐳 Run Web Server with Docker

```dockerfile
# Dockerfile.server (create this if you want to containerise the generator itself)
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5050
CMD ["python", "main.py", "--web", "--port", "5050"]
```

```bash
docker build -t project-gen .
docker run -p 5050:5050 project-gen
```

---

## 🔧 Install as CLI tool

```bash
pip install -e .

# Then use anywhere:
project-gen          # interactive CLI
project-gen-web      # web server
```

---

## 📖 After Generation – What to Edit

For every generated project, **the only files you need to edit** before running are:

### 1. `.env` (copy from `.env.example`)

Each project's `.env.example` is fully commented. The secrets you **must** change:

| Stack | Required secrets |
|-------|-----------------|
| Next.js | `DATABASE_URL`, `NEXTAUTH_SECRET` |
| React + Node | `MONGODB_URI`, `JWT_SECRET` |
| Django | `SECRET_KEY`, `DATABASE_URL` |
| Vue + Express | `DB_PASS`, `JWT_SECRET` |
| React Static | `VITE_API_KEY` (if using external APIs) |
| Electron | None – SQLite is local |

### 2. Nothing else is required to run

Everything else – routes, models, auth, Docker config – is pre-wired and ready.

---

## 🗺 Roadmap

- [ ] More stacks: Laravel, NestJS, FastAPI, Ruby on Rails
- [ ] Template customisation via YAML config file
- [ ] GitHub Actions CI/CD files per stack
- [ ] `--no-git` and `--no-docker` CLI flags
- [ ] Plugin system for custom stacks

---

## 📄 License

MIT – use freely in personal and commercial projects.
