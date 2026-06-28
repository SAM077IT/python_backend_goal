# 🧰 Git & GitHub Interview Prep
### Python Developer · 4 Years Experience

> **How to use:** Click any question to expand the answer. Questions are ordered from foundational → advanced within each section. Real-world examples reference a Django e-commerce project (Martify).

---

## 📋 Table of Contents

| # | Section |
|---|---------|
| 1 | [Git Internals & Core Concepts](#1-git-internals--core-concepts) |
| 2 | [Branching & Merging Strategies](#2-branching--merging-strategies) |
| 3 | [Rebasing & History Rewriting](#3-rebasing--history-rewriting) |
| 4 | [Git Workflows](#4-git-workflows) |
| 5 | [Stashing, Tagging & Refs](#5-stashing-tagging--refs) |
| 6 | [GitHub Features & Collaboration](#6-github-features--collaboration) |
| 7 | [GitHub Actions & CI/CD](#7-github-actions--cicd) |
| 8 | [Git Hooks](#8-git-hooks) |
| 9 | [Git in Django / Python Projects](#9-git-in-django--python-projects) |
| 10 | [Troubleshooting & Recovery](#10-troubleshooting--recovery) |
| 11 | [Advanced & Tricky Questions](#11-advanced--tricky-questions) |

---

## 1. Git Internals & Core Concepts

<details>
<summary><strong>Q1. What are the four types of Git objects? How do they relate to each other?</strong></summary>

Git is a **content-addressable filesystem**. Every piece of data is stored as a SHA-1-hashed object.

| Object | Description |
|--------|-------------|
| **blob** | Raw file content (no filename) |
| **tree** | Directory snapshot — maps names → blobs/trees |
| **commit** | Snapshot pointer — points to a tree + parent commit(s) + metadata |
| **tag** | Named, signed pointer to a commit |

```
commit (abc123)
 └── tree (def456)
      ├── blob (111) → "manage.py"
      ├── blob (222) → "requirements.txt"
      └── tree (333) → "martify/"
           ├── blob (444) → "__init__.py"
           └── blob (555) → "settings.py"
```

```bash
# Inspect any object
git cat-file -t abc123   # prints: commit
git cat-file -p abc123   # pretty-prints the commit object
```

</details>

---

<details>
<summary><strong>Q2. What is the difference between the working directory, staging area (index), and repository?</strong></summary>

```
Working Directory  →  Staging Area (Index)  →  Repository (.git)
   (files on disk)       git add                  git commit
```

| Zone | What it holds |
|------|--------------|
| **Working Directory** | Current files you're editing |
| **Index / Staging** | Snapshot of what the next commit will look like |
| **Repository** | Permanent object store; all commits live here |

```bash
git status          # shows differences across all three zones
git diff            # WD vs Index
git diff --staged   # Index vs last commit (HEAD)
git diff HEAD       # WD vs last commit (combined)
```

**Practical tip:** You can stage only part of a file:
```bash
git add -p martify/payments/views.py   # interactive hunk selection
```

</details>

---

<details>
<summary><strong>Q3. What exactly is HEAD in Git?</strong></summary>

`HEAD` is a symbolic reference — a pointer to the **currently checked-out branch or commit**.

```bash
cat .git/HEAD
# → ref: refs/heads/main          ← attached (normal)
# → 4a3f1b9c...                   ← detached HEAD
```

**Detached HEAD** happens when you `checkout` a specific commit instead of a branch:
```bash
git checkout 4a3f1b9c    # detached — no branch points here
git checkout -b hotfix   # re-attach by creating a new branch
```

`HEAD~1` = one commit behind HEAD  
`HEAD~3` = three commits behind HEAD  
`HEAD^2` = second parent of a merge commit

</details>

---

<details>
<summary><strong>Q4. What is the difference between git fetch, git pull, and git pull --rebase?</strong></summary>

```
git fetch origin        → downloads remote changes, does NOT modify local branches
git pull origin main    → fetch + merge (creates a merge commit if diverged)
git pull --rebase       → fetch + rebase (linear history, no extra merge commits)
```

**Diagram:**

```
Before pull:
  A - B - C  (local main)
            \
             D - E  (origin/main)

After git pull (merge):
  A - B - C - M  ← merge commit
            \ /
             D - E

After git pull --rebase:
  A - B - D - E - C'  ← C replayed on top
```

**Best practice in team Django projects:**
```bash
git config --global pull.rebase true   # always rebase on pull
```

</details>

---

<details>
<summary><strong>Q5. How does git store data differently from other VCS systems like SVN?</strong></summary>

| SVN / CVS | Git |
|-----------|-----|
| Stores **diffs** (what changed) | Stores **snapshots** (full state) |
| Central server required | Every clone is a full repository |
| Slow branching | Branching is nearly instant (just a pointer) |

Git tracks content, not files. Two identical files → same blob SHA. This makes storage efficient via **packfiles** (delta compression is applied during `git gc`, not at write time).

```bash
git count-objects -vH   # shows loose objects vs packed objects
git gc                  # manually trigger garbage collection + compression
```

</details>

---

## 2. Branching & Merging Strategies

<details>
<summary><strong>Q6. What is the difference between a fast-forward merge and a three-way merge?</strong></summary>

**Fast-forward merge** — only possible when the target branch has no new commits since the feature branched off:

```
main:    A - B
feature:         C - D

After: git checkout main && git merge feature
main:    A - B - C - D   (pointer just moves forward, no new commit)
```

**Three-way merge** — when both branches have diverged:

```
main:    A - B - E
feature:     C - D

After merge:
main:    A - B - E - M   (M is a new merge commit with two parents)
                 \   /
                  C-D
```

```bash
git merge feature-branch              # defaults to FF if possible
git merge --no-ff feature-branch      # always create a merge commit (useful for PRs)
git merge --squash feature-branch     # squash all commits into one staged change
```

**When to use `--no-ff`:** In GitFlow, merging feature → develop should always leave a merge commit so the branch history is visible.

</details>

---

<details>
<summary><strong>Q7. How do you resolve a merge conflict? Walk through a real example.</strong></summary>

**Scenario:** Two developers edited `martify/settings.py` on different branches.

```bash
git merge feature/add-stripe
# CONFLICT (content): Merge conflict in martify/settings.py
```

Git marks the file:
```python
<<<<<<< HEAD
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY_LIVE')
=======
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY_TEST')
>>>>>>> feature/add-stripe
```

**Resolution steps:**
```bash
# 1. Open the file and decide what the final code should be
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY', default='')

# 2. Remove all conflict markers

# 3. Stage the resolved file
git add martify/settings.py

# 4. Complete the merge
git commit   # Git auto-fills the merge commit message

# Optional: use a visual tool
git mergetool   # opens vimdiff / VS Code / IntelliJ depending on config
```

**Abort a conflict mid-way:**
```bash
git merge --abort
```

</details>

---

<details>
<summary><strong>Q8. What is git cherry-pick and when would you use it?</strong></summary>

`cherry-pick` applies a **specific commit** from one branch onto another without merging the whole branch.

```bash
git log feature/payments --oneline
# 7f3a1c2 Fix Stripe webhook signature validation
# 4e9b0d1 Add payment model
# a1b2c3d Update README

# You only want the webhook fix on main (hotfix scenario):
git checkout main
git cherry-pick 7f3a1c2
```

**Real-world use cases:**
- Backporting a security fix to a maintenance branch
- Picking a specific bugfix without taking in-progress feature work
- Recovering a useful commit from a deleted branch

```bash
# Cherry-pick a range of commits
git cherry-pick A..B          # commits after A up to B
git cherry-pick A^..B         # includes A

# Cherry-pick without committing (review first)
git cherry-pick --no-commit 7f3a1c2
```

</details>

---

<details>
<summary><strong>Q9. What does git diff between two branches show, and how is it different from git log?</strong></summary>

```bash
# Shows the LINE-LEVEL differences in file content
git diff main..feature/payments

# Shows only COMMIT history between branches
git log main..feature/payments --oneline

# What commits are on feature but not main?
git log main..feature/payments

# What's the common ancestor (merge base)?
git merge-base main feature/payments
```

**Useful diff flags:**
```bash
git diff --stat main..feature       # summary: files changed, insertions, deletions
git diff --name-only main..feature  # just filenames
git diff main..feature -- payments/ # scope to a specific directory
```

</details>

---

## 3. Rebasing & History Rewriting

<details>
<summary><strong>Q10. Explain git rebase. When would you use it over merge?</strong></summary>

**Rebase** moves or replays commits on top of another base commit, producing a **linear history**.

```
Before:
  main:    A - B - C
  feature:     D - E

git checkout feature
git rebase main

After:
  main:    A - B - C
  feature:         C - D' - E'  (D and E are replayed, get new SHA)
```

**Merge vs Rebase:**

| | Merge | Rebase |
|--|-------|--------|
| History | Preserves divergence | Linear, clean |
| Merge commit | Yes | No |
| Rewrites SHA | No | Yes (rebased commits get new SHAs) |
| Safe for shared branches | ✅ Yes | ❌ No — never rebase a public/shared branch |

**When to rebase:**
- Local feature branch before opening a PR
- Keeping a feature branch up to date with `main`

```bash
git checkout feature/stripe-payments
git rebase origin/main     # replay feature commits on top of latest main
git push --force-with-lease   # required after rebase (SHAs changed)
```

**`--force-with-lease` vs `--force`:**  
`--force-with-lease` only force-pushes if no one else has pushed since your last fetch — safer.

</details>

---

<details>
<summary><strong>Q11. What is interactive rebase and what can you do with it?</strong></summary>

```bash
git rebase -i HEAD~5   # open last 5 commits interactively
```

Editor opens:
```
pick a1b2c3 Add Stripe model
pick 4d5e6f WIP: working on webhook
pick 7g8h9i Fix typo in webhook
pick 0j1k2l Add webhook tests
pick 3m4n5o Update docs
```

**Commands you can apply to each commit:**

| Command | Effect |
|---------|--------|
| `pick` | Keep as-is |
| `reword` (r) | Keep commit, edit message |
| `edit` (e) | Pause to amend the commit |
| `squash` (s) | Meld into previous commit, combine messages |
| `fixup` (f) | Meld into previous, discard this message |
| `drop` (d) | Delete this commit entirely |
| `reorder` | Just move lines to reorder commits |

**Common workflow before a PR:**
```bash
# Squash WIP commits into clean logical commits
pick a1b2c3 Add Stripe model
squash 4d5e6f WIP: working on webhook
squash 7g8h9i Fix typo in webhook
pick 0j1k2l Add webhook tests
reword 3m4n5o Update docs
```

</details>

---

<details>
<summary><strong>Q12. What is the difference between git reset, git revert, and git restore?</strong></summary>

**git reset** — moves HEAD (and optionally the index/WD):

```bash
git reset --soft HEAD~1    # undo last commit, keep changes STAGED
git reset --mixed HEAD~1   # undo last commit, keep changes in WD (default)
git reset --hard HEAD~1    # undo last commit, DISCARD all changes ⚠️
```

**git revert** — creates a NEW commit that undoes a previous one (safe for shared branches):

```bash
git revert 4a3f1b9c        # new commit that reverses 4a3f1b9c
git revert HEAD~3..HEAD    # revert last 3 commits
```

**git restore** — restores file content (doesn't touch commits):

```bash
git restore martify/settings.py           # discard WD changes (replaces old `git checkout -- file`)
git restore --staged martify/settings.py  # unstage (replaces old `git reset HEAD file`)
```

**Decision tree:**
```
Did you push already?
  YES → use git revert (safe, doesn't rewrite history)
  NO  → use git reset (cleaner, rewrites history locally)
```

</details>

---

<details>
<summary><strong>Q13. What is git reflog and when does it save you?</strong></summary>

`reflog` is Git's **safety net** — it records every time HEAD moves, even during resets, rebases, or branch deletions.

```bash
git reflog
# 4a3f1b9 HEAD@{0}: reset: moving to HEAD~3
# 7c8d9e0 HEAD@{1}: commit: Add Stripe webhook
# 1a2b3c4 HEAD@{2}: commit: Add payment model
# ...
```

**Recovery scenarios:**

```bash
# Accidentally ran git reset --hard and lost commits
git reflog
# Find the SHA of the lost commit
git checkout -b recovery-branch 7c8d9e0

# Accidentally deleted a branch
git reflog
git checkout -b deleted-feature 7c8d9e0

# Reset after a bad rebase
git reflog
git reset --hard HEAD@{4}
```

Reflog entries expire after 90 days (configurable via `gc.reflogExpire`).

</details>

---

## 4. Git Workflows

<details>
<summary><strong>Q14. Explain GitFlow. What are its branches and when is each used?</strong></summary>

GitFlow is a branching model suited for **versioned releases**.

```
main         ── production-ready code, tagged releases
develop      ── integration branch for features
feature/*    ── individual features branched from develop
release/*    ── stabilisation before a release (bugfixes only)
hotfix/*     ── urgent fixes branched from main
```

**Lifecycle:**
```bash
# Start a feature
git checkout develop
git checkout -b feature/product-recommendations

# Finish a feature
git checkout develop
git merge --no-ff feature/product-recommendations
git branch -d feature/product-recommendations

# Prepare a release
git checkout develop
git checkout -b release/1.2.0
# fix bugs, bump version
git checkout main
git merge --no-ff release/1.2.0
git tag -a v1.2.0 -m "Release 1.2.0"
git checkout develop
git merge --no-ff release/1.2.0

# Hotfix
git checkout main
git checkout -b hotfix/fix-payment-crash
# fix it
git checkout main && git merge --no-ff hotfix/fix-payment-crash
git checkout develop && git merge --no-ff hotfix/fix-payment-crash
```

**When NOT to use GitFlow:** Small teams, continuous deployment → prefer GitHub Flow or trunk-based development.

</details>

---

<details>
<summary><strong>Q15. What is GitHub Flow and how does it differ from GitFlow?</strong></summary>

**GitHub Flow** — simpler, designed for **continuous deployment**:

```
1. Branch from main
2. Make commits
3. Open a Pull Request
4. Review & discuss
5. Deploy from the branch (optional)
6. Merge to main
```

```bash
git checkout -b feature/cart-api
# ...make changes...
git push -u origin feature/cart-api
# → open PR on GitHub → review → merge → auto-deploy
```

**GitFlow vs GitHub Flow:**

| | GitFlow | GitHub Flow |
|--|---------|-------------|
| Long-lived branches | develop, release, hotfix | Only main |
| Release process | Formal release branches | Deploy on merge to main |
| Best for | Versioned software | SaaS / continuous delivery |
| Complexity | High | Low |

Most Django SaaS teams use GitHub Flow or a light variant of it.

</details>

---

<details>
<summary><strong>Q16. What is trunk-based development?</strong></summary>

All developers commit (or merge short-lived branches) **directly to main/trunk**, multiple times per day. Feature flags control what users see.

```python
# settings.py
FEATURE_FLAGS = {
    'new_checkout_flow': env.bool('FF_NEW_CHECKOUT', default=False),
}

# views.py
if settings.FEATURE_FLAGS['new_checkout_flow']:
    return CheckoutV2View.as_view()(request)
return CheckoutV1View.as_view()(request)
```

**Benefits:**
- No long-lived branches → no integration hell
- CI runs on every commit to main
- Forces small, focused commits

**Risk:** Requires discipline, comprehensive CI, and mature feature-flag infrastructure.

</details>

---

## 5. Stashing, Tagging & Refs

<details>
<summary><strong>Q17. How does git stash work? What are common stash commands?</strong></summary>

`git stash` saves your uncommitted changes (WD + index) to a stack, giving you a clean working directory.

```bash
git stash                        # stash WD + staged changes
git stash push -m "WIP: cart API refactor"  # named stash
git stash -u                     # include untracked files
git stash -a                     # include ignored files too

git stash list
# stash@{0}: On feature/cart: WIP: cart API refactor
# stash@{1}: On main: hotfix temp work

git stash pop                    # apply latest + remove from stack
git stash apply stash@{1}        # apply specific, keep in stack
git stash drop stash@{0}         # remove without applying
git stash clear                  # drop all stashes

# Create a branch from a stash (useful if WD diverged)
git stash branch feature/cart stash@{0}
```

</details>

---

<details>
<summary><strong>Q18. What are Git tags and what is the difference between lightweight and annotated tags?</strong></summary>

Tags mark specific points in history — typically release versions.

**Lightweight tag** — just a pointer (like a branch that doesn't move):
```bash
git tag v1.0.0
```

**Annotated tag** — a full Git object with tagger info, date, message, and optional GPG signature:
```bash
git tag -a v1.0.0 -m "First stable release of Martify"
git tag -s v1.0.0 -m "Signed release"   # GPG signed
```

**Working with tags:**
```bash
git tag                          # list all tags
git tag -l "v1.*"                # filter
git show v1.0.0                  # inspect annotated tag
git push origin v1.0.0           # push a specific tag
git push origin --tags           # push all tags
git tag -d v1.0.0                # delete locally
git push origin --delete v1.0.0  # delete remote
```

**Always use annotated tags for releases** — they show who tagged it and when, and `git describe` uses them for version strings.

</details>

---

<details>
<summary><strong>Q19. What is the difference between origin, upstream, and fork in Git?</strong></summary>

```
upstream  =  original project repo (e.g. django/django)
origin    =  your fork on GitHub
local     =  your machine
```

**Open source contribution workflow:**
```bash
# Fork on GitHub → then:
git clone https://github.com/sami/martify.git   # origin = your fork
git remote add upstream https://github.com/org/martify.git

git remote -v
# origin   https://github.com/sami/martify.git (fetch)
# upstream https://github.com/org/martify.git  (fetch)

# Keep fork in sync
git fetch upstream
git checkout main
git rebase upstream/main
git push origin main
```

</details>

---

## 6. GitHub Features & Collaboration

<details>
<summary><strong>Q20. What should a good Pull Request description include?</strong></summary>

A PR is a communication tool as much as a code submission. Good PRs include:

```markdown
## What does this PR do?
Adds Stripe webhook handler for `payment_intent.succeeded` events.
Updates Order status to 'paid' and triggers confirmation email.

## Why?
Closes #142 — orders were not being marked paid on async Stripe events.

## Changes
- `payments/webhooks.py` — new WebhookHandler class
- `payments/urls.py` — added `/webhooks/stripe/` endpoint
- `payments/tests/test_webhooks.py` — 12 new test cases

## How to test
1. Run `stripe listen --forward-to localhost:8000/webhooks/stripe/`
2. Trigger: `stripe trigger payment_intent.succeeded`
3. Confirm order status changes to 'paid' in admin

## Screenshots / Output
[attach if UI changes]

## Checklist
- [x] Tests added / updated
- [x] Migrations included
- [x] `.env.example` updated
- [x] No secrets committed
```

</details>

---

<details>
<summary><strong>Q21. What is the difference between Squash, Merge, and Rebase merge strategies on GitHub PRs?</strong></summary>

GitHub offers three merge buttons:

**Merge commit** (`git merge --no-ff`):
- Preserves all commits + adds a merge commit
- Full history visible, noisier
- Best for: large features where individual commits matter

**Squash and merge** (`git merge --squash`):
- All PR commits → one commit on main
- Clean main history, loses granular feature history
- Best for: small features, WIP-heavy branches

**Rebase and merge** (`git rebase`):
- All PR commits placed linearly on main (no merge commit)
- SHAs change
- Best for: teams that want linear history without squashing

```bash
# Equivalent CLI commands:
git merge --no-ff feature             # Merge commit
git merge --squash feature && git commit  # Squash
git rebase feature && git merge --ff-only # Rebase
```

</details>

---

<details>
<summary><strong>Q22. How do you protect the main branch on GitHub and why?</strong></summary>

Branch protection rules prevent accidental or unauthorized pushes.

**Settings → Branches → Branch protection rules → Add rule for `main`:**

| Rule | Purpose |
|------|---------|
| Require pull request before merging | No direct pushes |
| Require N approvals | Enforces peer review |
| Require status checks to pass | CI must be green |
| Require branches to be up to date | No stale PRs |
| Restrict who can push | Only specific teams |
| Require signed commits | GPG verification |
| Require linear history | No merge commits (forces squash/rebase) |

**In a Django project, typical status checks:**
- `pytest` (unit + integration tests)
- `flake8` / `ruff` (linting)
- `black --check` (formatting)
- `mypy` (type checking)
- Docker build check

</details>

---

<details>
<summary><strong>Q23. What are GitHub Environments and how are they used in deployment?</strong></summary>

GitHub Environments let you define deployment targets (`staging`, `production`) with protection rules and secrets scoped to each environment.

```yaml
# .github/workflows/deploy.yml
jobs:
  deploy-staging:
    environment: staging       # uses STAGING_* secrets
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: ./deploy.sh
        env:
          SECRET_KEY: ${{ secrets.STAGING_SECRET_KEY }}

  deploy-production:
    environment: production    # requires manual approval
    needs: deploy-staging
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: ./deploy.sh
        env:
          SECRET_KEY: ${{ secrets.PROD_SECRET_KEY }}
```

**Environment protection rules:**
- Required reviewers (must approve before job runs)
- Wait timer (e.g. 5 min delay before production deploy)
- Restrict to specific branches (only `main` can deploy to production)

</details>

---

<details>
<summary><strong>Q24. What is a GitHub Action and how is it triggered?</strong></summary>

A GitHub Action is an automated workflow defined in `.github/workflows/*.yml`. It can be triggered by:

```yaml
on:
  push:                         # any push
    branches: [main, develop]
  pull_request:                 # PR opened/updated
    branches: [main]
  schedule:                     # cron
    - cron: '0 2 * * *'        # 2 AM daily
  workflow_dispatch:            # manual trigger via GitHub UI
  release:
    types: [published]          # on new release
```

**Anatomy:**
```
Workflow (.yml file)
  └── Job (runs on a runner)
       └── Step (individual command or action)
            ├── run: shell command
            └── uses: action from marketplace
```

</details>

---

## 7. GitHub Actions & CI/CD

<details>
<summary><strong>Q25. Write a complete GitHub Actions CI workflow for a Django + pytest project.</strong></summary>

```yaml
# .github/workflows/ci.yml
name: Django CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: martify_test
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
        ports: ['5432:5432']
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements/test.txt

      - name: Run linting
        run: |
          ruff check .
          black --check .

      - name: Run type checks
        run: mypy martify/

      - name: Run migrations
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/martify_test
          DJANGO_SETTINGS_MODULE: martify.settings.test
          SECRET_KEY: test-secret-key
        run: python manage.py migrate

      - name: Run tests
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/martify_test
          DJANGO_SETTINGS_MODULE: martify.settings.test
          SECRET_KEY: test-secret-key
          STRIPE_SECRET_KEY: ${{ secrets.STRIPE_TEST_KEY }}
        run: |
          pytest --cov=martify --cov-report=xml -v

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          file: ./coverage.xml
```

</details>

---

<details>
<summary><strong>Q26. How do you cache dependencies in GitHub Actions to speed up CI?</strong></summary>

```yaml
# Method 1: Built-in cache with setup-python (recommended)
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
    cache: 'pip'                  # caches pip cache dir keyed to requirements files

# Method 2: Manual cache control
- name: Cache pip dependencies
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-

# Cache Docker layers
- name: Cache Docker layers
  uses: actions/cache@v4
  with:
    path: /tmp/.buildx-cache
    key: ${{ runner.os }}-buildx-${{ github.sha }}
    restore-keys: |
      ${{ runner.os }}-buildx-
```

**Key insight:** The `hashFiles()` function creates a cache key based on file contents. If `requirements.txt` doesn't change, the cache is reused entirely.

</details>

---

<details>
<summary><strong>Q27. How do you securely use secrets in GitHub Actions? What are common mistakes?</strong></summary>

```yaml
# ✅ Correct: Use ${{ secrets.NAME }}
- name: Deploy
  env:
    SECRET_KEY: ${{ secrets.DJANGO_SECRET_KEY }}
    DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
  run: python manage.py deploy

# ✅ Pass as argument
- run: ./deploy.sh
  env:
    API_KEY: ${{ secrets.API_KEY }}
```

**Common mistakes:**

```yaml
# ❌ Never hardcode secrets
env:
  SECRET_KEY: "my-super-secret-key"

# ❌ Never echo secrets (GitHub masks them but still bad practice)
run: echo "Key is ${{ secrets.SECRET_KEY }}"

# ❌ Never store secrets in repository files (.env committed to git)
```

**Secret scopes:**
- **Repository secrets** — available to all workflows in one repo
- **Environment secrets** — scoped to `staging` or `production` environments
- **Organization secrets** — shared across repos in an org

**Rotate secrets after any potential exposure.** Use `GITHUB_TOKEN` (auto-provisioned) for inter-repo actions instead of personal access tokens where possible.

</details>

---

<details>
<summary><strong>Q28. How do you build and push a Docker image in GitHub Actions?</strong></summary>

```yaml
name: Build & Push Docker Image

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            samidev/martify:latest
            samidev/martify:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Deploy to server
        run: |
          ssh -o StrictHostKeyChecking=no ${{ secrets.DEPLOY_USER }}@${{ secrets.DEPLOY_HOST }} \
            "docker pull samidev/martify:${{ github.sha }} && docker-compose up -d"
```

</details>

---

## 8. Git Hooks

<details>
<summary><strong>Q29. What are Git hooks? Name and describe the most commonly used ones.</strong></summary>

Git hooks are scripts that Git executes **automatically** at specific points in the workflow. They live in `.git/hooks/`.

| Hook | Trigger | Common Use |
|------|---------|-----------|
| `pre-commit` | Before commit is created | Linting, formatting, tests |
| `commit-msg` | After commit message is entered | Enforce message format |
| `post-commit` | After commit is made | Notifications |
| `pre-push` | Before push to remote | Run full test suite |
| `pre-rebase` | Before rebase begins | Safety checks |
| `post-merge` | After a merge | Install new dependencies |
| `post-checkout` | After checkout | Activate virtualenv, run migrations |

```bash
ls .git/hooks/
# applypatch-msg.sample  pre-commit.sample  ...
```

**Make a hook executable:**
```bash
cp .git/hooks/pre-commit.sample .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

</details>

---

<details>
<summary><strong>Q30. Write a pre-commit hook for a Django project that runs linting and tests.</strong></summary>

```bash
#!/bin/bash
# .git/hooks/pre-commit

set -e   # exit on first error

echo "🔍 Running pre-commit checks..."

# 1. Check for debug statements
if grep -rn "import pdb\|pdb.set_trace\|breakpoint()" --include="*.py" .; then
  echo "❌ Found debug statements. Remove before committing."
  exit 1
fi

# 2. Check for print statements in non-test files
if grep -rn "^\s*print(" --include="*.py" . | grep -v "tests/"; then
  echo "⚠️  Found print() statements in production code."
  read -p "Commit anyway? [y/N] " -n 1 -r
  echo
  [[ ! $REPLY =~ ^[Yy]$ ]] && exit 1
fi

# 3. Run Black formatter check
echo "⬛ Checking Black formatting..."
black --check .

# 4. Run Ruff linter
echo "⚡ Running Ruff..."
ruff check .

# 5. Run Django system checks
echo "🦄 Running Django system checks..."
python manage.py check --deploy 2>/dev/null || python manage.py check

echo "✅ All pre-commit checks passed!"
```

**Better approach: use pre-commit framework (industry standard)**

```bash
pip install pre-commit
```

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.3.0
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.1
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-merge-conflict
      - id: detect-private-key
      - id: check-added-large-files
```

```bash
pre-commit install         # installs hooks into .git/hooks/
pre-commit run --all-files # run on everything manually
```

</details>

---

## 9. Git in Django / Python Projects

<details>
<summary><strong>Q31. What should be in a Django project's .gitignore?</strong></summary>

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.so
*.egg
*.egg-info/
dist/
build/
.eggs/
.Python

# Virtual environments
venv/
env/
.venv/
ENV/

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
/static/           # collected static files
/media/            # user uploads

# Environment variables — CRITICAL
.env
.env.*
!.env.example      # keep the template

# Secrets — NEVER commit these
*.pem
*.key
*.cert

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Testing
.pytest_cache/
.coverage
htmlcov/
coverage.xml
.tox/

# Docker
.docker/

# Terraform / Infra (if applicable)
*.tfstate
*.tfstate.*
.terraform/

# Node (if you have frontend)
node_modules/
npm-debug.log*
```

</details>

---

<details>
<summary><strong>Q32. How should Django database migrations be handled in Git?</strong></summary>

**Always commit migrations.** They are version-controlled schema history.

```bash
git add martify/payments/migrations/0005_add_webhook_event.py
git commit -m "Add WebhookEvent model migration"
```

**Handling migration conflicts (two devs created 0005 simultaneously):**

```bash
git pull origin develop
# CONFLICT: both added migrations/0005_*.py

# Option 1: Merge migrations
python manage.py makemigrations --merge --name merge_0005

# Option 2: Recreate your migration on top
git checkout origin/develop -- martify/payments/migrations/0005_their_migration.py
python manage.py makemigrations payments
# Your migration becomes 0006
```

**Best practices:**
- One migration per logical change
- Never squash migrations that are already in production
- Name migrations meaningfully: `python manage.py makemigrations --name add_stripe_customer_id`
- Review migration files in PR — they touch the production database

**In CI, always run:**
```bash
python manage.py migrate --check   # fails if unapplied migrations exist
python manage.py migrate           # apply in test/staging environments
```

</details>

---

<details>
<summary><strong>Q33. How do you manage environment-specific settings with Git?</strong></summary>

**Never commit `.env` files.** Use a template:

```bash
# .env.example (committed to git — no real values)
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgres://user:pass@localhost:5432/martify
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
```

```bash
# .env (local, in .gitignore — real values)
SECRET_KEY=django-insecure-abc123...
DEBUG=True
DATABASE_URL=postgres://sami:password@localhost:5432/martify_dev
```

**Django settings pattern:**
```python
# martify/settings/base.py    ← committed, no secrets
# martify/settings/local.py   ← gitignored or in .env
# martify/settings/staging.py ← committed, reads from env
# martify/settings/production.py ← committed, reads from env

# Use python-decouple or django-environ
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```

**If a secret is accidentally committed:**
```bash
# Immediately rotate/revoke the secret
# Remove from history (note: history rewrite — coordinate with team)
git filter-repo --path .env --invert-paths
# Force push
git push --force --all
# Notify team to re-clone
```

</details>

---

<details>
<summary><strong>Q34. How would you use Git bisect to find a bug in a Django project?</strong></summary>

`git bisect` performs a **binary search** through commit history to find which commit introduced a bug.

**Scenario:** Stripe payments stopped working somewhere in the last 50 commits.

```bash
# Start bisect
git bisect start

# Mark current state as bad
git bisect bad

# Mark a known good commit (last release)
git bisect good v1.3.0

# Git checks out the midpoint commit automatically
# Run your test to check if bug exists
python manage.py test payments.tests.test_stripe

# Tell git the result
git bisect good    # or git bisect bad

# Git keeps halving — repeat until it finds the culprit:
# "4a3f1b9 is the first bad commit"

# Done
git bisect reset   # return to HEAD

# Automate it
git bisect run python manage.py test payments.tests.test_stripe
# Git runs the command at each step automatically
```

`log₂(50) ≈ 6` — only 6 steps to find the bad commit among 50!

</details>

---

## 10. Troubleshooting & Recovery

<details>
<summary><strong>Q35. How do you undo a commit that has already been pushed to a shared branch?</strong></summary>

**Never use `git reset --hard` + force push on a shared branch.** Use `git revert` instead.

```bash
# Revert a single commit (creates a new "undo" commit)
git revert 4a3f1b9c
git push origin main

# Revert a merge commit (need -m to specify mainline parent)
git revert -m 1 4a3f1b9c   # -m 1 = keep the first parent (main branch)
git push origin main

# Revert multiple commits (in reverse order to avoid conflicts)
git revert HEAD~3..HEAD
# Or interactively:
git revert --no-commit HEAD~3..HEAD
git commit -m "Revert last 3 commits: removed broken payment flow"
```

**If it's your own branch (not shared yet):**
```bash
git reset --hard HEAD~1
git push --force-with-lease origin feature/my-branch
```

</details>

---

<details>
<summary><strong>Q36. How do you recover a deleted branch?</strong></summary>

```bash
# Find the SHA from reflog
git reflog --all | grep "feature/deleted-branch"
# or
git log --all --oneline | head -20

# Recreate the branch
git checkout -b feature/deleted-branch 7c8d9e0

# If deleted on remote but still local
git push origin feature/deleted-branch

# If deleted both locally and remotely (within retention period)
# Check GitHub's PR page — the SHA is still there
git fetch origin 7c8d9e0   # may work depending on GitHub's object retention
git checkout -b feature/deleted-branch FETCH_HEAD
```

</details>

---

<details>
<summary><strong>Q37. How do you fix "Your branch has diverged from origin" error?</strong></summary>

This means your local branch and the remote branch both have commits the other doesn't:

```
      A - B - C (origin/main)
     /
... D - E - F (local main)
```

**Options:**

```bash
# Option 1: Merge (safe, creates merge commit)
git pull origin main     # merge by default

# Option 2: Rebase (cleaner, rewrites local commits)
git pull --rebase origin main

# Option 3: If you're sure YOUR local commits are wrong
git reset --hard origin/main   # ⚠️ discards local commits

# Option 4: If you're sure YOUR commits are right and remote is wrong
git push --force-with-lease origin main   # ⚠️ only on YOUR branch
```

**Prevent this:** Regularly pull/rebase on long-running branches. Communicate with teammates before force-pushing.

</details>

---

## 11. Advanced & Tricky Questions

<details>
<summary><strong>Q38. What is git worktree and when is it useful for a Django developer?</strong></summary>

`git worktree` lets you have **multiple working directories** from the same repository simultaneously — each checked out to a different branch.

```bash
# Check out a hotfix branch without disrupting current work
git worktree add ../martify-hotfix hotfix/payment-crash
cd ../martify-hotfix
# Full working copy — can run server, tests, etc.
python manage.py runserver 8001

# Back in main directory
cd ../martify
# main branch still intact, no stashing needed

# Remove when done
git worktree remove ../martify-hotfix
```

**Use cases:**
- Fix a production bug while in the middle of a feature
- Run two branches of your Django app side-by-side for comparison
- Long-running test suite on branch A while you code on branch B

</details>

---

<details>
<summary><strong>Q39. What is git submodule vs git subtree?</strong></summary>

Both let you include another repository inside your repository.

**Git Submodule:**
- The sub-repo is referenced by a specific commit SHA (not copied)
- `.gitmodules` file tracks the URL and path
- Cloners must run `git submodule update --init --recursive`

```bash
git submodule add https://github.com/org/martify-shared-utils.git shared/
git submodule update --remote   # pull latest from submodule
```

**Git Subtree:**
- Sub-repo content is copied INTO your repo
- No special clone step needed
- Simpler for consumers, more complex to push changes back

```bash
git subtree add --prefix=shared/ https://github.com/org/shared.git main --squash
git subtree pull --prefix=shared/ https://github.com/org/shared.git main --squash
git subtree push --prefix=shared/ https://github.com/org/shared.git main
```

| | Submodule | Subtree |
|--|-----------|---------|
| History | Separate | Merged |
| Clone complexity | Needs `--recursive` | None |
| Contribute back | Easy | Possible but complex |
| Best for | Shared libraries you don't modify | Code you'll fork/modify |

</details>

---

<details>
<summary><strong>Q40. How does GitHub's CODEOWNERS file work?</strong></summary>

`CODEOWNERS` automatically requests review from specific people/teams when files they own are changed in a PR.

```
# .github/CODEOWNERS

# Global owners (fallback)
*                    @sami @lead-dev

# Django settings and config — tech lead must review
martify/settings/    @tech-lead
.github/             @devops-team

# Payments are sensitive — two people must review
martify/payments/    @payments-lead @senior-dev

# Database migrations — always needs DBA review
*/migrations/        @dba-team @tech-lead

# Frontend
martify/templates/   @frontend-team
martify/static/      @frontend-team

# Documentation
docs/               @tech-writer
*.md                @tech-writer
```

**Requires:** Branch protection rule — "Require review from Code Owners" must be enabled for CODEOWNERS to be enforced.

</details>

---

<details>
<summary><strong>Q41. What is git blame and how do you use it effectively?</strong></summary>

`git blame` shows who last modified each line of a file and in which commit.

```bash
git blame martify/payments/views.py

# Output:
# 4a3f1b9c (Sami  2024-03-15 10:23:45 +0530 42) def process_payment(request):
# 7c8d9e01 (Alice 2024-02-20 09:11:30 +0530 43)     amount = request.data['amount']

# Blame a specific range of lines
git blame -L 40,60 martify/payments/views.py

# Show the full commit hash
git blame --show-stats martify/payments/views.py

# Ignore whitespace changes
git blame -w martify/payments/views.py

# Follow file through renames
git blame --follow martify/payments/views.py
```

**VS Code:** The GitLens extension provides inline git blame in the editor.

**GitHub:** Click any line → "View git blame" in the file view.

**Note:** `git blame` shows *last* modifier, not original author. Use `git log -S "search_term"` (pickaxe) to find who introduced specific code.

</details>

---

<details>
<summary><strong>Q42. Explain the difference between git clone --depth and a full clone. When would you use a shallow clone?</strong></summary>

**Full clone:** Downloads the entire history of the repository.

**Shallow clone (`--depth N`):** Downloads only the last N commits — no full history.

```bash
# Shallow clone (last 1 commit) — common in CI
git clone --depth 1 https://github.com/sami/martify.git

# Shallow clone with more history
git clone --depth 50 https://github.com/sami/martify.git

# Unshallow (fetch full history later)
git fetch --unshallow
```

**Speeds up GitHub Actions significantly:**
```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 1    # shallow clone (default is 1 in actions/checkout@v4)
    # fetch-depth: 0 for full history (needed for git describe, versioning)
```

**When you need full history (`fetch-depth: 0`):**
- `git describe` for version strings
- `git log` for changelog generation
- `git bisect`
- Coverage tools that compare branches

</details>

---

*Last updated: June 2026 · Tailored for Python/Django · 4 Years Experience*
