# Docker & CI/CD Interview Prep
> Tailored to your resume: Docker containerization, Jenkins CI/CD pipelines, automated testing & deployment

---

## Table of Contents
- [Docker Fundamentals](#docker-fundamentals)
- [Docker Compose](#docker-compose)
- [CI/CD with Jenkins](#cicd-with-jenkins)
- [Best Practices](#best-practices)
- [Scenario-Based Questions](#scenario-based-questions)

---

## Docker Fundamentals

<details>
<summary><strong>1. What is Docker and why did you use it in your projects?</strong></summary>

### Answer

Docker is a containerization platform that packages your application + all its dependencies into a portable, isolated container.

**Why Docker for your Django projects:**
- **Consistency:** "Works on my machine" → works everywhere (dev, staging, prod)
- **Isolation:** App runs in its own environment, no conflicts with other apps
- **Reproducibility:** Same container image in dev and production
- **Scalability:** Easy to spin up more containers behind a load balancer
- **CI/CD:** Containers make automated build/test/deploy pipelines simple

```
Without Docker:                    With Docker:
Dev machine:  Python 3.9          Container:    Python 3.11
Staging:      Python 3.11  →      Container:    Python 3.11
Production:   Python 3.10         Container:    Python 3.11
              (inconsistent!)                    (consistent!)
```

**Key Docker concepts:**
- **Image:** Read-only template (like a class)
- **Container:** Running instance of an image (like an object)
- **Dockerfile:** Recipe for building an image
- **Registry:** Store for images (Docker Hub, AWS ECR)
- **Volume:** Persistent storage outside container lifecycle
- **Network:** Communication between containers

```bash
# Basic commands
docker build -t martify:latest .           # build image
docker run -d -p 8000:8000 martify:latest  # run container
docker ps                                   # list running containers
docker logs martify-web                     # view logs
docker exec -it martify-web bash           # shell into container
docker stop martify-web                    # stop container
docker image prune                         # cleanup unused images
```

</details>

---

<details>
<summary><strong>2. Walk me through the Dockerfile you wrote for your Django application.</strong></summary>

### Answer

```dockerfile
# Multi-stage build — reduces final image size significantly
# Stage 1: Builder — install dependencies
FROM python:3.11-slim as builder

WORKDIR /app

# Prevent .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \           # psycopg2 requires libpq
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies to user directory
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Production image — copy only what's needed
FROM python:3.11-slim

WORKDIR /app

# Copy only the installed packages from builder
COPY --from=builder /root/.local /root/.local

# Install only runtime dependencies (not build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \              # runtime PostgreSQL client library
    && rm -rf /var/lib/apt/lists/*

# Create non-root user — security best practice
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy application code
COPY --chown=appuser:appuser . .

# Run as non-root user
USER appuser

# Set environment
ENV PYTHONPATH=/app
ENV PATH=/root/.local/bin:$PATH
ENV DJANGO_SETTINGS_MODULE=martify.settings.production

# Collect static files at build time
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health/ || exit 1

# Start command
CMD ["gunicorn", "martify.wsgi:application",
     "--bind", "0.0.0.0:8000",
     "--workers", "4",
     "--timeout", "120",
     "--keep-alive", "5",
     "--access-logfile", "-",
     "--error-logfile", "-"]
```

```bash
# .dockerignore — don't copy these into image
.git
.gitignore
.env
.env.*
*.pyc
__pycache__
*.log
node_modules
.DS_Store
docs/
tests/
*.md
Dockerfile*
docker-compose*

# Result: final image ~200MB instead of ~800MB
```

</details>

---

## Docker Compose

<details>
<summary><strong>3. Explain your docker-compose setup for the full Django stack.</strong></summary>

### Answer

```yaml
# docker-compose.yml — full production-like local environment
version: '3.9'

services:
  # Django web application
  web:
    build:
      context: .
      dockerfile: Dockerfile
    command: gunicorn martify.wsgi:application --bind 0.0.0.0:8000 --workers 4 --reload
    volumes:
      - .:/app                    # mount code for development hot-reload
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    env_file:
      - .env
    environment:
      - DJANGO_SETTINGS_MODULE=martify.settings.development
    depends_on:
      db:
        condition: service_healthy    # wait for DB to be ready
      redis:
        condition: service_healthy
    ports:
      - "8000:8000"
    restart: unless-stopped

  # Celery worker — background tasks
  celery:
    build: .
    command: celery -A martify worker --loglevel=info --concurrency=4 -Q default,emails,reports
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - db
      - redis
    restart: unless-stopped

  # Celery Beat — periodic tasks scheduler
  celery-beat:
    build: .
    command: celery -A martify beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - db
      - redis
    restart: unless-stopped

  # Flower — Celery monitoring UI
  flower:
    build: .
    command: celery -A martify flower --port=5555
    ports:
      - "5555:5555"
    env_file:
      - .env
    depends_on:
      - redis

  # PostgreSQL database
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: martify_db
      POSTGRES_USER: martify_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql   # initial SQL
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U martify_user -d martify_db"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Redis — cache + message broker
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Nginx — reverse proxy + static files
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/staticfiles:ro
      - media_volume:/media:ro
    depends_on:
      - web
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  static_volume:
  media_volume:

networks:
  default:
    driver: bridge
```

```bash
# Common docker-compose commands
docker-compose up -d                          # start all services
docker-compose up -d web celery               # start specific services
docker-compose exec web python manage.py migrate  # run migrations
docker-compose exec web python manage.py createsuperuser
docker-compose logs -f web                    # follow logs
docker-compose down -v                        # stop + remove volumes
docker-compose build --no-cache               # force rebuild
```

</details>

---

## CI/CD with Jenkins

<details>
<summary><strong>4. Walk me through the CI/CD pipeline you built with Jenkins and Docker.</strong></summary>

### Answer

```groovy
// Jenkinsfile — declarative pipeline
pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'registry.martify.com'
        IMAGE_NAME = 'martify-backend'
        IMAGE_TAG = "${BUILD_NUMBER}-${GIT_COMMIT.take(7)}"
        FULL_IMAGE = "${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
        DEPLOY_SERVER = 'ec2-production.martify.com'
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git log --oneline -5'
            }
        }

        stage('Code Quality') {
            parallel {
                stage('Lint') {
                    steps {
                        sh '''
                            pip install flake8 black isort
                            flake8 . --max-line-length=100 --exclude=migrations
                            black --check .
                            isort --check-only .
                        '''
                    }
                }
                stage('Type Check') {
                    steps {
                        sh 'mypy martify/ --ignore-missing-imports'
                    }
                }
            }
        }

        stage('Test') {
            environment {
                DATABASE_URL = 'postgresql://test:test@localhost:5432/test_db'
                DJANGO_SETTINGS_MODULE = 'martify.settings.test'
            }
            steps {
                sh '''
                    # Start test DB
                    docker-compose -f docker-compose.test.yml up -d db

                    # Run tests with coverage
                    pytest \
                        --cov=. \
                        --cov-report=xml \
                        --cov-report=html \
                        --cov-fail-under=80 \
                        --junitxml=test-results.xml \
                        -v

                    # Check for unapplied migrations
                    python manage.py migrate --check
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                    publishCoverage adapters: [coberturaAdapter('coverage.xml')]
                    sh 'docker-compose -f docker-compose.test.yml down'
                }
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                    pip install bandit safety
                    bandit -r martify/ -ll       # static security analysis
                    safety check                  # check for known vulnerabilities
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    docker build \
                        --build-arg BUILD_NUMBER=${BUILD_NUMBER} \
                        --build-arg GIT_COMMIT=${GIT_COMMIT} \
                        -t ${FULL_IMAGE} \
                        -t ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest \
                        .
                """
            }
        }

        stage('Push to Registry') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-registry',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                        echo $DOCKER_PASS | docker login ${DOCKER_REGISTRY} -u $DOCKER_USER --password-stdin
                        docker push ${FULL_IMAGE}
                        docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest
                    """
                }
            }
        }

        stage('Deploy to Staging') {
            when { branch 'develop' }
            steps {
                deployToEnvironment('staging', FULL_IMAGE)
                runSmokeTests('https://staging.martify.com')
            }
        }

        stage('Deploy to Production') {
            when { branch 'main' }
            input {
                message "Deploy to production?"
                ok "Deploy"
                submitter "senior-devs,tech-leads"
            }
            steps {
                deployToEnvironment('production', FULL_IMAGE)
                runSmokeTests('https://martify.com')
            }
        }
    }

    post {
        success {
            slackSend(
                color: 'good',
                message: "✅ Deploy ${IMAGE_TAG} to ${BRANCH_NAME} succeeded"
            )
        }
        failure {
            slackSend(
                color: 'danger',
                message: "❌ Build ${BUILD_NUMBER} failed on ${BRANCH_NAME}. <${BUILD_URL}|View>"
            )
            emailext(
                to: 'team@martify.com',
                subject: "Build Failed: ${JOB_NAME} #${BUILD_NUMBER}",
                body: "Build failed. Check: ${BUILD_URL}"
            )
        }
        always {
            sh 'docker image prune -f'   // cleanup old images
            cleanWs()
        }
    }
}

def deployToEnvironment(String env, String image) {
    withCredentials([sshUserPrivateKey(
        credentialsId: 'deploy-key',
        keyFileVariable: 'SSH_KEY'
    )]) {
        sh """
            ssh -i $SSH_KEY -o StrictHostKeyChecking=no deploy@${DEPLOY_SERVER} '
                docker pull ${image}
                docker-compose -f /var/www/martify/docker-compose.prod.yml up -d --no-deps web celery
                docker-compose exec web python manage.py migrate --noinput
                docker-compose exec web python manage.py collectstatic --noinput
            '
        """
    }
}

def runSmokeTests(String baseUrl) {
    sh """
        curl -f ${baseUrl}/api/health/ || exit 1
        curl -f ${baseUrl}/api/v1/products/ || exit 1
        echo "Smoke tests passed!"
    """
}
```

</details>

---

## Best Practices

<details>
<summary><strong>5. What Docker and CI/CD best practices do you follow?</strong></summary>

### Answer

```python
# Docker best practices:

# 1. Multi-stage builds — smaller images
# Dev image: 800MB → Production image: 180MB

# 2. Non-root user
RUN useradd -r -u 1001 appuser
USER appuser

# 3. .dockerignore — exclude everything you don't need
# Reduces build context size, speeds up builds

# 4. Layer caching — copy requirements first, code second
COPY requirements.txt .        # rarely changes → cached
RUN pip install -r requirements.txt
COPY . .                       # changes frequently → cache invalidated only here

# 5. Pin base image versions
FROM python:3.11.8-slim        # exact version, not 'latest'

# 6. One process per container
# NOT: one container running Nginx + Gunicorn + Celery
# YES: separate containers for each, orchestrated by compose/K8s

# 7. Health checks
HEALTHCHECK --interval=30s --timeout=5s \
    CMD curl -f http://localhost:8000/api/health/ || exit 1

# 8. Read-only filesystem where possible
docker run --read-only --tmpfs /tmp martify:latest
```

```yaml
# CI/CD best practices:

# 1. Fast feedback — put quick checks first
# Order: lint → unit tests → integration tests → build → deploy

# 2. Fail fast — if lint fails, don't run tests
# (Jenkins parallel stages achieve this)

# 3. Environment parity — use Docker so test env = prod env

# 4. Deployment strategies:
#    Blue-Green: run new version alongside old, switch traffic
#    Rolling: replace instances one by one
#    Canary: send 5% traffic to new version first

# 5. Secrets management — never in Jenkinsfile or code
# Use Jenkins Credentials, AWS Secrets Manager, or HashiCorp Vault

# 6. Rollback strategy
def rollback(String previousImage):
    sh "docker-compose up -d --no-deps web ${previousImage}"

# 7. Post-deployment smoke tests — verify before declaring success

# 8. Branch strategy:
# feature/* → PR → develop (auto-deploy to staging)
# develop → main (manual deploy to production)
```

</details>

---

## Scenario-Based Questions

<details>
<summary><strong>6. Your Docker container is running out of memory in production. How do you debug it?</strong></summary>

### Answer

```bash
# Step 1: Identify memory usage
docker stats martify-web               # live stats
docker inspect martify-web | grep -i memory  # container limits

# Step 2: Inside the container
docker exec -it martify-web bash
top                                    # process memory
cat /proc/meminfo                      # system memory

# Step 3: Python memory profiling
pip install memory_profiler tracemalloc

# In the view or task that's leaking
import tracemalloc

tracemalloc.start()
run_suspicious_function()
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)

# Step 4: Identify common leak sources in Django
# - Large querysets loaded into memory (missing .iterator())
# - Celery tasks accumulating in memory
# - Global state growing unboundedly
# - Django DEBUG=True in production (stores all SQL queries in memory!)

# Step 5: Set container memory limits
# docker-compose.yml
services:
  web:
    deploy:
      resources:
        limits:
          memory: 512M          # OOM kill if exceeds
          cpus: '1.0'
        reservations:
          memory: 256M
          cpus: '0.5'

# Step 6: Fix the leak
# Missing .iterator() on large queryset
for order in Order.objects.all().iterator(chunk_size=1000):   # not .all()!
    process(order)

# Celery: configure result expiry
CELERY_RESULT_EXPIRES = 3600   # 1 hour
```

</details>

---

<details>
<summary><strong>7. A deployment broke production. How do you rollback?</strong></summary>

### Answer

```bash
# Step 1: Detect (monitoring alerts within seconds)
# CloudWatch alarm → PagerDuty/Slack alert → On-call engineer

# Step 2: Assess
# Are errors increasing? 5xx rate? Response time spike?
# Are new pods/containers failing health checks?

# Step 3: Immediate rollback (< 5 minutes)

# Docker/Compose — rollback to previous image
docker-compose -f docker-compose.prod.yml up -d --no-deps \
    -e IMAGE_TAG=previous-working-tag \
    web celery

# Or tag: always tag known-good releases
docker tag martify:latest martify:stable

# Rollback to stable
docker run -d martify:stable

# Step 4: Database migrations — the hard part
# If migration is reversible:
python manage.py migrate orders 0012   # roll back to migration before the bad one

# If not reversible: restore from RDS snapshot (LAST RESORT)
# RDS Console → Snapshots → Restore to point in time

# Step 5: Communicate
# Update status page → notify users → internal Slack

# Step 6: Post-mortem (blameless)
# What failed? Why? Timeline of events
# How to prevent it? What monitoring was missing?

# Prevention:
# 1. Always tag Docker images with version
# 2. Test migrations on a DB clone before production
# 3. Use backward-compatible migrations first, then remove old code
# 4. Blue-green deployment — keep old environment running
# 5. Smoke tests after every deploy
```

</details>

