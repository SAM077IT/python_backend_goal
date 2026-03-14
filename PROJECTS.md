# 🏗️ Project Ideas + Status

> Build real projects. Deploy them. Put the live URL on your resume and LinkedIn.

---

## 📌 Recommended Projects (Pick by Phase)

---

### 🟦 Phase 2 Project — Django REST API

**Project: Blog / Bookmark API**

A clean REST API with authentication.

**Features:**
- User registration and login (Token auth via DRF)
- CRUD for blog posts or bookmarks
- Categories / Tags (ManyToMany)
- Search functionality
- Pagination
- PostgreSQL backend

**Tech Stack:** Django + DRF + PostgreSQL

**Why this project?**
It covers every core concept interviewers ask about: ORM, relationships, serializers, auth, filtering.

| Task | Status |
|------|--------|
| Set up Django project with PostgreSQL | ⬜ |
| Create User model + Token auth | ⬜ |
| Build CRUD API with DRF | ⬜ |
| Add filtering + pagination | ⬜ |
| Write basic tests | ⬜ |
| Push to GitHub with good README | ⬜ |

---

### 🟨 Phase 3 Project — FastAPI + Docker

**Project: Task Manager API (with JWT Auth)**

A production-style REST API.

**Features:**
- User registration + JWT login
- Task CRUD (title, description, priority, due date, status)
- Assign tasks to users
- Filter tasks by status / priority
- Containerized with Docker Compose

**Tech Stack:** FastAPI + SQLAlchemy + PostgreSQL + Docker

**Why this project?**
FastAPI with JWT + Docker is the exact stack Indian startups hire for in 2026.

| Task | Status |
|------|--------|
| Set up FastAPI project structure | ⬜ |
| SQLAlchemy models + Alembic migrations | ⬜ |
| JWT Auth (register + login) | ⬜ |
| Task CRUD endpoints | ⬜ |
| Dockerize with docker-compose | ⬜ |
| Write tests with pytest | ⬜ |
| Push to GitHub with README | ⬜ |

---

### 🟩 Phase 4 (Main) Project — Full Deployable App

**Pick ONE of the following:**

---

#### Option A: URL Shortener Service
- User accounts + link management
- Short URL generation (unique slug)
- Click analytics (count, timestamps)
- FastAPI + PostgreSQL + Redis (for caching)
- Deploy on Render or Railway

#### Option B: Job Board API
- Companies post jobs
- Candidates apply
- Filter by location, salary, tech stack
- Django + DRF + PostgreSQL
- Full authentication for both roles

#### Option C: E-commerce Product API
- Products, Categories, Orders, Cart
- User auth + role-based access (admin vs customer)
- Django + DRF + PostgreSQL
- Image upload support (Django Storages / S3)

#### Option D: Real-time Chat Backend (Advanced)
- WebSocket support
- Django Channels + Redis
- Room-based messaging
- Great differentiator if you can pull it off

---

## 🚀 Deployment Options (All Free Tier)

| Platform | Best For | Notes |
|----------|----------|-------|
| [Render.com](https://render.com) | Django + FastAPI | Free tier, easy setup |
| [Railway.app](https://railway.app) | FastAPI + PostgreSQL | Good for Docker deploys |
| [Fly.io](https://fly.io) | Docker apps | More control |
| [Vercel](https://vercel.com) | Frontend only | Not for Python backends |
| [Supabase](https://supabase.com) | PostgreSQL hosting | Free managed DB |

---

## ✅ Project Quality Checklist (Before Adding to Resume)

- [ ] README explains what the project does, how to run it locally, and tech stack
- [ ] No hardcoded secrets (use `.env` + `python-decouple`)
- [ ] `.env.example` file included
- [ ] API has proper error responses (4xx, 5xx with JSON messages)
- [ ] At least basic unit tests exist
- [ ] Deployed and live URL in README
- [ ] Commit history looks real (not one giant commit)

---

*Pro tip: Quality > quantity. One well-built, deployed project is worth more than five half-finished ones.*
