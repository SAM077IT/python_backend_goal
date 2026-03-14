# 🐍 Python Backend Developer — 3-Month Job Roadmap

> **Profile:** Intermediate Python | 3–4 hrs/day | Target: Job in 3 Months | Location: Kolkata, India  
> **Last Updated:** March 2026

---

## 🎯 Goal

Land a Python Backend / Full-Stack Developer job at an Indian company within **90 days**.

---

## 📐 How This Repo Is Structured

```
python_backend_goal/
│
├── README.md               ← This file (master roadmap)
├── SKILLS.md               ← Full skill list with free resources
├── DAILY_LOG.md            ← Your daily progress tracker
├── PROJECTS.md             ← Project ideas + status
└── INTERVIEW_PREP.md       ← DSA + interview question bank
```

---

## 🗓️ 3-Month Phase Overview

| Phase | Duration | Focus |
|-------|----------|-------|
| **Phase 1** | Week 1–2 | Python Deep Dive + Git + Linux Basics |
| **Phase 2** | Week 3–5 | Django + PostgreSQL + REST APIs |
| **Phase 3** | Week 6–7 | FastAPI + Docker + Auth (JWT) |
| **Phase 4** | Week 8–9 | Project Build (Deploy a real app) |
| **Phase 5** | Week 10–11 | DSA + Interview Prep |
| **Phase 6** | Week 12 | Apply + Portfolio Polish |

---

## 📅 Phase-by-Phase Breakdown

---

### ✅ Phase 1 — Solidify Python Foundations (Week 1–2)

**Why:** Even intermediate devs have gaps. Indian interviewers love Python internals.

#### Topics to Cover
- OOP: classes, inheritance, dunder methods, `__init__`, `__str__`
- Decorators, generators, context managers
- List comprehensions, lambda, `map`, `filter`
- File I/O, exception handling, logging
- Virtual environments (`venv`), `pip`, `requirements.txt`
- Git: branching, commits, pull requests, `.gitignore`
- Linux/terminal basics: `cd`, `ls`, `grep`, `chmod`, `ssh`

#### Daily Schedule (3–4 hrs)
| Time | Activity |
|------|----------|
| 1 hr | Read / watch one concept |
| 1 hr | Practice on paper or in REPL |
| 1 hr | Solve 1 LeetCode Easy in Python |
| 30 min | Commit notes to this repo |

#### Resources
- [Python OOP – Corey Schafer (YouTube)](https://www.youtube.com/watch?v=ZDa-Z5JzLYM)
- [Real Python – Decorators](https://realpython.com/primer-on-python-decorators/)
- [Git – The Simple Guide](https://rogerdudler.github.io/git-guide/)
- [Missing Semester – Linux CLI](https://missing.csail.mit.edu/)

#### ✔️ Phase 1 Checklist
- [ ] Can explain decorators and give an example
- [ ] Comfortable with OOP (class, inherit, super())
- [ ] Repo on GitHub with first commit
- [ ] Solved 10 LeetCode Easy problems in Python

---

### ✅ Phase 2 — Django + PostgreSQL + REST APIs (Week 3–5)

**Why:** Django is the #1 demanded framework in Indian job listings.

#### Topics to Cover
- Django project structure (MVT pattern)
- Models, Migrations, Django ORM (queries, filters, related objects)
- Django Admin
- Views (FBV + CBV), URLs, Templates
- Django REST Framework (DRF): Serializers, ViewSets, Routers
- Authentication: Session auth + Token auth
- PostgreSQL: setup, connect to Django via `psycopg2`
- Database relationships: OneToOne, ForeignKey, ManyToMany
- `.env` files for secrets (`python-decouple`)

#### Daily Schedule (3–4 hrs)
| Time | Activity |
|------|----------|
| 1.5 hrs | Follow Django tutorial / build feature |
| 1 hr | Set up PostgreSQL locally, practice raw SQL |
| 1 hr | Build the Phase 2 project (see PROJECTS.md) |
| 30 min | DSA problem (easy/medium) |

#### Resources
- [Django Official Tutorial](https://docs.djangoproject.com/en/5.0/intro/tutorial01/)
- [DRF Official Docs](https://www.django-rest-framework.org/)
- [CS50 Web with Django (Free – edX)](https://cs50.harvard.edu/web/2020/)
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- [Simple is Better Than Complex – DRF](https://simpleisbetterthancomplex.com/)

#### ✔️ Phase 2 Checklist
- [ ] Built a Django app with models + migrations
- [ ] Created a working REST API with DRF
- [ ] Connected Django to PostgreSQL (not SQLite)
- [ ] API has authentication (token or session)
- [ ] Project is on GitHub

---

### ✅ Phase 3 — FastAPI + Docker + JWT Auth (Week 6–7)

**Why:** FastAPI is rapidly rising in Indian startups and product companies.

#### Topics to Cover
- FastAPI basics: routes, path params, query params, request body
- Pydantic models for validation
- SQLAlchemy ORM with FastAPI + PostgreSQL
- Async endpoints (`async def`)
- JWT Authentication (python-jose, passlib)
- Docker: Dockerfile, docker-compose, volumes, networks
- Docker Compose with FastAPI + PostgreSQL

#### Resources
- [FastAPI Official Docs / Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI – The Complete Course 2026 (Udemy)](https://www.udemy.com/course/fastapi-the-complete-course/) *(paid, often ₹400–600 on sale)*
- [FastAPI + PostgreSQL + Docker Tutorial](https://blog.primerpy.com/2026/01/04/fastapi/integrating-postgresql-with-fastapi/)
- [Docker for Beginners – TechWorld with Nana (YouTube)](https://www.youtube.com/watch?v=3c-iBn73dDE)

#### ✔️ Phase 3 Checklist
- [ ] Built a FastAPI app with CRUD endpoints
- [ ] JWT login + protected routes working
- [ ] App runs inside Docker containers
- [ ] docker-compose up brings up API + DB together

---

### ✅ Phase 4 — Build & Deploy a Real Project (Week 8–9)

**Why:** Indian interviewers always ask "show me something you built." A deployed project = instant credibility.

#### Choose ONE project from PROJECTS.md and:
1. Build it end-to-end (backend only or full-stack)
2. Write proper README with setup instructions
3. Dockerize it
4. Deploy it (free tier: Render, Railway, or Fly.io)
5. Add the live URL to your GitHub and LinkedIn

#### Must-Have Features in the Project
- User registration + login (JWT)
- At least 3 database models with relationships
- Full CRUD REST API
- Input validation + error handling
- Environment variables (no hardcoded secrets)
- Basic unit tests

#### Resources
- [Render.com – Free Deploy](https://render.com/)
- [Railway.app – Free Deploy](https://railway.app/)
- [pytest – Official Docs](https://docs.pytest.org/)

---

### ✅ Phase 5 — DSA + Interview Prep (Week 10–11)

**Why:** Indian companies (even startups) have at least 1 DSA round.

#### DSA Topics (Priority Order)
1. Arrays & Strings
2. HashMaps & Sets
3. Two Pointers & Sliding Window
4. Stack & Queue
5. Linked Lists
6. Binary Search
7. Recursion & Backtracking
8. Trees (BFS, DFS)
9. Dynamic Programming (basic)
10. Sorting algorithms

#### Interview Theory Topics
- Python internals: GIL, garbage collection, memory management
- OOP: SOLID principles, design patterns
- REST API design best practices
- WSGI vs ASGI
- SQL: JOINs, indexing, EXPLAIN query
- Redis basics (caching, pub/sub)
- HTTP: status codes, headers, cookies vs JWT
- OS basics: processes, threads, concurrency

#### Resources
- [LeetCode – NeetCode 150 List](https://neetcode.io/roadmap)
- [GeeksforGeeks – DSA for Interviews](https://www.geeksforgeeks.org/dsa/top-100-data-structure-and-algorithms-dsa-interview-questions-topic-wise/)
- [InterviewBit – Python Questions](https://www.interviewbit.com/python-interview-questions/)
- [Second Talent – Python Backend Interview Qs](https://www.secondtalent.com/interview-guide/python/)
- [System Design Primer (GitHub)](https://github.com/donnemartin/system-design-primer)

#### Daily Schedule (Week 10–11)
| Time | Activity |
|------|----------|
| 1 hr | 2 LeetCode problems (easy/medium) |
| 1 hr | Study one theory topic |
| 1 hr | Mock interview (use Pramp / peer) |
| 30 min | Polish resume/LinkedIn |

---

### ✅ Phase 6 — Apply + Portfolio Polish (Week 12)

**Why:** You now have the skills. This week is about packaging and maximizing conversion.

#### Resume Tips
- Keep it 1 page
- Lead with your deployed project with live URL
- Quantify things: "Built REST API serving X endpoints", "Reduced query time by X%"
- Include: Python, Django, FastAPI, PostgreSQL, Docker, Git, REST APIs, JWT

#### Where to Apply (India)
- **Naukri.com** — Highest volume, set job alerts for "Python Developer", "Backend Developer Python"
- **LinkedIn Jobs** — Set Easy Apply filters; connect with hiring managers
- **Internshala** — Good for entry-level / fresher roles
- **AngelList / Wellfound** — Startups, often faster hiring
- **Cutshort.io** — Indian tech startup-focused
- **GitHub Jobs / Remote** — For remote-first companies
- **Direct applications** — Freshworks, Razorpay, Meesho, Groww, Zepto all hire Python devs

#### Profile Polish
- [ ] GitHub profile: pinned repos, good READMEs, consistent commit history
- [ ] LinkedIn: headline = "Python Backend Developer | Django | FastAPI | Docker"
- [ ] Add deployed project link everywhere
- [ ] Get 2–3 recommendations on LinkedIn

---

## 💡 Key Principles

1. **Build, don't just watch.** For every tutorial, build something alongside it.
2. **Commit daily.** Even small commits. GitHub green squares matter to recruiters.
3. **One deployed project beats 10 unfinished ones.**
4. **DSA is non-negotiable.** Even product startups test it.
5. **Track your progress.** Use `DAILY_LOG.md` every single day.

---

## 📊 Progress Tracker

| Phase | Status | Start Date | End Date |
|-------|--------|------------|----------|
| Phase 1 – Python Foundations | ⏳ Not Started | | |
| Phase 2 – Django + PostgreSQL | ⏳ Not Started | | |
| Phase 3 – FastAPI + Docker | ⏳ Not Started | | |
| Phase 4 – Project Build | ⏳ Not Started | | |
| Phase 5 – DSA + Interview Prep | ⏳ Not Started | | |
| Phase 6 – Apply | ⏳ Not Started | | |

---

*This roadmap was generated based on 2026 Indian job market research. Update it as you progress.*
