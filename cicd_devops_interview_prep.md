# CI/CD, Docker, Jenkins & AWS — Interview Prep Guide
> **Role:** Python Backend Developer · **Domain:** Martify (Django + PostgreSQL + Stripe)  
> **Resume claim:** *"Automated build, testing, and deployment processes by implementing CI/CD pipelines using Docker and Jenkins"*

---

## Table of Contents

1. [CI/CD — The Big Picture](#1-cicd--the-big-picture)
2. [Docker — Containers for Python/Django](#2-docker--containers-for-pythondjango)
3. [Jenkins — Pipeline Automation](#3-jenkins--pipeline-automation)
4. [AWS EC2 — Compute](#4-aws-ec2--compute)
5. [AWS S3 — Object Storage](#5-aws-s3--object-storage)
6. [AWS RDS — Managed Database](#6-aws-rds--managed-database)
7. [AWS IAM — Identity & Access Management](#7-aws-iam--identity--access-management)
8. [End-to-End Flow: Martify Deployment](#8-end-to-end-flow-martify-deployment)
9. [Quick-Fire Interview Q&A](#9-quick-fire-interview-qa)

---

## 1. CI/CD — The Big Picture

### What It Is

| Term | Meaning | Practical outcome |
|------|---------|-------------------|
| **CI** – Continuous Integration | Every code push is automatically built and tested | Bugs caught within minutes, not days |
| **CD** – Continuous Delivery | Artifact is always ready to deploy (one-click) | Stable build always available |
| **CD** – Continuous Deployment | Every green build goes to production automatically | Zero-touch releases |

### Pipeline Stages (remember this pattern)

```
Code Push → Lint/Format → Unit Tests → Build Image → Push to Registry → Deploy to Staging → Smoke Test(build verification testing) → Deploy to Production
```

### Why It Reduces Production Issues (resume talking point)

- **Shift-left testing** — failures caught at PR time, not in production
- **Reproducible builds** — Docker image is identical in dev, staging, and prod
- **Rollback** — if a deploy fails, the previous image is re-tagged and redeployed in seconds
- **Audit trail** — every Jenkins build log is a deployment record

### Interview Q&A

<details>
<summary><strong>Q: What is the difference between CI and CD?</strong></summary>

> CI is the practice of merging code frequently and validating each merge with automated builds and tests. CD extends this by keeping the codebase always deployable (Continuous Delivery) or automatically deploying every green build (Continuous Deployment). In Martify, CI ran pytest and flake8 on every PR. CD then built a Docker image and deployed to the EC2 staging environment automatically, requiring a manual approval gate before production.

</details>

<details>
<summary><strong>Q: How does CI/CD reduce production issues?</strong></summary>

> First, tests run on every commit, so regressions are caught early. Second, the same Docker image that passed tests is what gets deployed—no "works on my machine" problems. Third, because deploys happen frequently in small increments, any issue is easy to isolate and the blast radius is small. In my experience, moving to automated pipelines reduced emergency hotfixes significantly because flawed code was never reaching production undetected.

</details>

---

## 2. Docker — Containers for Python/Django

### Core Concepts

| Concept | What it is | Analogy |
|---------|-----------|---------|
| **Image** | Read-only blueprint | Python class |
| **Container** | Running instance of an image | Instance of a class |
| **Dockerfile** | Build instructions for an image | Recipe |
| **docker-compose** | Orchestrates multiple containers | `docker run` for a whole app stack |
| **Volume** | Persistent storage outside the container | External hard drive |
| **Network** | Bridge between containers | Private LAN |

### Dockerfile for Martify

```dockerfile
# ── Build stage ──────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Install deps in a separate layer so they cache independently
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Runtime stage ─────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Copy pre-built packages from builder
COPY --from=builder /install /usr/local

# Copy app code
COPY . .

# Never run as root inside a container
RUN adduser --disabled-password --gecos "" appuser
USER appuser

EXPOSE 8000

# Use gunicorn in production
CMD ["gunicorn", "martify.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
```

**Key things to explain in an interview:**
- `python:3.11-slim` — minimal base image; smaller attack surface and faster pulls
- Multi-stage build — `builder` installs deps, `runtime` copies only the result; final image has no pip/gcc
- `USER appuser` — principle of least privilege; root inside a container = root on the host if breakout occurs
- Layer caching — `COPY requirements.txt .` before `COPY . .` means code changes don't bust the dep cache

### docker-compose for Local Dev

```yaml
# docker-compose.yml
version: "3.9"

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app                        # hot-reload: local code mounts into container
    ports:
      - "8000:8000"
    environment:
      - DEBUG=1
      - DATABASE_URL=postgres://martify:secret@db:5432/martify
      - STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}
    depends_on:
      db:
        condition: service_healthy    # wait until postgres is ready

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data  # data persists across restarts
    environment:
      POSTGRES_DB: martify
      POSTGRES_USER: martify
      POSTGRES_PASSWORD: secret
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U martify"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### Common Docker Commands (know these cold)

```bash
# Build
docker build -t martify:latest .
docker build --no-cache -t martify:1.0.0 .

# Run
docker run -d -p 8000:8000 --env-file .env martify:latest
docker run --rm -it martify:latest bash   # interactive debug shell

# Compose
docker-compose up -d              # start all services detached
docker-compose logs -f web        # tail web service logs
docker-compose exec web bash      # shell into running web container
docker-compose down -v            # stop and delete volumes

# Inspect
docker ps -a                      # all containers including stopped
docker images                     # list local images
docker inspect <container_id>     # full JSON metadata
docker stats                      # live CPU/mem per container

# Cleanup
docker system prune -af           # remove all unused images/containers/networks
```

### Interview Q&A

<details>
<summary><strong>Q: What is the difference between a Docker image and a container?</strong></summary>

> An image is an immutable, layered snapshot defined by a Dockerfile — think of it as a class. A container is a running (or stopped) instance of that image — like an object. You can run many containers from one image, each with its own isolated process, filesystem, and network. In Martify, the CI pipeline built one image per commit and tagged it with the Git SHA. Jenkins then spun up a container from that image to run tests, and the same image was deployed to EC2.

</details>

<details>
<summary><strong>Q: Why use multi-stage builds?</strong></summary>

> Multi-stage builds let you use one image for compiling/installing (which needs build tools like gcc, pip, etc.) and a separate, leaner image for runtime. Only the compiled artifacts are copied into the final stage. For Martify, this shrunk the production image from ~900 MB to ~180 MB, which means faster ECR pushes, faster EC2 pulls, and a smaller attack surface since there's no pip or compiler in production.

</details>

<details>
<summary><strong>Q: How do you handle secrets in Docker?</strong></summary>

> Never bake secrets into the image. Approaches in increasing security:
> 1. **Environment variables** at `docker run` time via `--env-file .env` (file never committed to git)
> 2. **AWS Secrets Manager / SSM Parameter Store** — app fetches secrets at startup via boto3
> 3. **Docker secrets** (Swarm) or **Kubernetes secrets** mounted as files  
> 
> In Martify's production setup, `DATABASE_URL` and `STRIPE_SECRET_KEY` are stored in AWS SSM Parameter Store and fetched by the Django settings module using `boto3.client('ssm').get_parameter()` with `WithDecryption=True`.

</details>

<details>
<summary><strong>Q: How does Docker networking work between containers?</strong></summary>

> By default, docker-compose puts all services on a shared bridge network. Each service is reachable by its service name as a hostname. So in Martify, the `web` container connects to the database at `db:5432` — Docker's internal DNS resolves `db` to the container's IP. This means no hardcoded IP addresses, and the network is isolated from the host.

</details>

---

## 3. Jenkins — Pipeline Automation

### Core Concepts

| Concept | Description |
|---------|-------------|
| **Pipeline** | The full CI/CD workflow defined in a `Jenkinsfile` |
| **Stage** | A named phase — Build, Test, Deploy |
| **Step** | A single command/action inside a stage |
| **Agent** | Where the pipeline runs — `agent any` or a Docker container |
| **Credential** | Secrets stored in Jenkins, injected via `withCredentials` |
| **Artifact** | File output from a build (reports, images) |
| **Webhook** | GitHub calls Jenkins on every push to trigger a build |

### Jenkinsfile for Martify (Declarative Pipeline)

```groovy
// Jenkinsfile
pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        IMAGE_NAME    = "martify"
        ECR_REGISTRY  = "123456789.dkr.ecr.ap-south-1.amazonaws.com"
        AWS_REGION    = "ap-south-1"
        // Jenkins credential IDs
        AWS_CREDS     = credentials('aws-ecr-credentials')
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                sh 'echo "Branch: ${GIT_BRANCH}, Commit: ${GIT_COMMIT}"'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    pip install --no-cache-dir -r requirements.txt
                    pip install pytest pytest-django flake8 coverage
                '''
            }
        }

        stage('Lint') {
            steps {
                sh 'flake8 . --max-line-length=120 --exclude=migrations'
            }
        }

        stage('Test') {
            environment {
                DATABASE_URL = 'sqlite:///test.db'    // in-memory equivalent for CI
                DJANGO_SETTINGS_MODULE = 'martify.settings.test'
            }
            steps {
                sh '''
                    coverage run -m pytest tests/ -v --tb=short
                    coverage report --fail-under=80
                    coverage xml -o coverage.xml
                '''
            }
            post {
                always {
                    // Publish coverage report in Jenkins UI
                    publishCoverage adapters: [coberturaAdapter('coverage.xml')]
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def imageTag = "${ECR_REGISTRY}/${IMAGE_NAME}:${GIT_COMMIT[0..6]}"
                    sh "docker build -t ${imageTag} ."
                    env.IMAGE_TAG = imageTag
                }
            }
        }

        stage('Push to ECR') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-ecr-credentials'
                ]]) {
                    sh '''
                        aws ecr get-login-password --region ${AWS_REGION} \
                          | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                        docker push ${IMAGE_TAG}
                        docker tag ${IMAGE_TAG} ${ECR_REGISTRY}/${IMAGE_NAME}:latest
                        docker push ${ECR_REGISTRY}/${IMAGE_NAME}:latest
                    '''
                }
            }
        }

        stage('Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                withCredentials([sshUserPrivateKey(
                    credentialsId: 'ec2-staging-key',
                    keyFileVariable: 'SSH_KEY'
                )]) {
                    sh '''
                        ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no \
                            ubuntu@${STAGING_HOST} \
                            "docker pull ${IMAGE_TAG} && \
                             docker stop martify || true && \
                             docker run -d --rm --name martify \
                               -p 8000:8000 \
                               --env-file /home/ubuntu/martify.env \
                               ${IMAGE_TAG}"
                    '''
                }
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            // Requires a human to click "Proceed" in Jenkins UI
            input {
                message "Deploy to production?"
                ok "Go Live"
            }
            steps {
                withCredentials([sshUserPrivateKey(
                    credentialsId: 'ec2-prod-key',
                    keyFileVariable: 'SSH_KEY'
                )]) {
                    sh '''
                        ssh -i ${SSH_KEY} ubuntu@${PROD_HOST} \
                            "docker pull ${IMAGE_TAG} && \
                             docker stop martify || true && \
                             docker run -d --rm --name martify \
                               -p 8000:8000 \
                               --env-file /home/ubuntu/martify.env \
                               ${IMAGE_TAG}"
                    '''
                }
            }
        }
    }

    post {
        failure {
            // Notify on Slack or email
            mail to: 'dev@martify.com',
                 subject: "BUILD FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "Check Jenkins: ${env.BUILD_URL}"
        }
        success {
            echo "Pipeline completed successfully. Image: ${env.IMAGE_TAG}"
        }
        always {
            cleanWs()  // clean workspace after every run
        }
    }
}
```

### Jenkins Key Concepts to Explain

**`when` directive** — conditional stage execution:
```groovy
when { branch 'main' }           // only on main
when { changeRequest() }         // only on PRs
when { environment name: 'DEPLOY_ENV', value: 'prod' }
```

**`post` block** — runs after pipeline regardless of outcome:
```groovy
post {
    always   { cleanWs() }          // always clean
    success  { /* notify slack */ }
    failure  { /* send alert */ }
    unstable { /* tests failed */ }
}
```

**Credentials binding** — secrets never appear in logs:
```groovy
withCredentials([string(credentialsId: 'stripe-key', variable: 'STRIPE_SK')]) {
    sh 'echo $STRIPE_SK'   // Jenkins masks this in console output as ****
}
```

### Interview Q&A

<details>
<summary><strong>Q: What is a Jenkinsfile and why is it important?</strong></summary>

> A Jenkinsfile is a Groovy-based DSL file committed to the repository that defines the entire pipeline as code. Storing it in source control means: the pipeline is version-controlled alongside the code, every team member can see and review CI/CD changes, and pipelines are reproducible across Jenkins instances. It's the difference between a fragile GUI-configured pipeline and one that can be recreated from scratch in minutes.

</details>

<details>
<summary><strong>Q: How do you handle environment-specific deployments in Jenkins?</strong></summary>

> Using the `when` directive on each stage. In Martify, pushes to `develop` auto-deploy to staging, while `main` requires a manual approval `input` step before production. Credentials for each environment are stored as separate Jenkins credentials (different SSH keys for staging and prod EC2 instances) and injected via `withCredentials`, so the Jenkinsfile never contains actual secrets.

</details>

<details>
<summary><strong>Q: How does Jenkins trigger a build on code push?</strong></summary>

> Via a webhook. In GitHub, you configure a webhook that POSTs to `http://<jenkins-host>/github-webhook/` on push events. Jenkins receives this, identifies the matching pipeline by repository URL, and starts the build. Alternatively, Jenkins can poll SCM on a schedule using `pollSCM('H/5 * * * *')`, but webhooks are preferred because they're instant and don't waste resources.

</details>

---

## 4. AWS EC2 — Compute

### What It Is

EC2 (Elastic Compute Cloud) provides virtual machines (instances) on AWS. For a Django app like Martify, EC2 hosts the running Docker containers.

### Key Concepts

| Concept | What to know |
|---------|-------------|
| **Instance type** | `t3.micro` (free tier, 1 vCPU, 1 GB RAM) → `t3.medium` for production |
| **AMI** | Amazon Machine Image — the OS template (Ubuntu 22.04 LTS is common) |
| **Security Group** | Stateful firewall at the instance level — controls inbound/outbound traffic |
| **Key Pair** | SSH authentication — `.pem` file you download once on creation |
| **Elastic IP** | Static public IP that persists across instance stops/starts |
| **User Data** | Startup script that runs once when the instance first boots |

### Security Group for Martify

```
Inbound Rules:
  Port 22  (SSH)   — Source: My IP only (not 0.0.0.0/0)
  Port 80  (HTTP)  — Source: 0.0.0.0/0
  Port 443 (HTTPS) — Source: 0.0.0.0/0
  Port 8000        — Source: Security Group of ALB only (not public)

Outbound Rules:
  All traffic — 0.0.0.0/0  (instance can call external APIs like Stripe)
```

### EC2 User Data (bootstrap script)

```bash
#!/bin/bash
# Runs on first boot — installs Docker so Jenkins can deploy immediately
apt-get update -y
apt-get install -y docker.io awscli
systemctl start docker
systemctl enable docker
usermod -aG docker ubuntu

# Pull latest image and start Martify
aws ecr get-login-password --region ap-south-1 \
  | docker login --username AWS --password-stdin 123456789.dkr.ecr.ap-south-1.amazonaws.com

docker pull 123456789.dkr.ecr.ap-south-1.amazonaws.com/martify:latest
docker run -d -p 8000:8000 \
  --env-file /home/ubuntu/martify.env \
  --name martify \
  123456789.dkr.ecr.ap-south-1.amazonaws.com/martify:latest
```

### Interview Q&A

<details>
<summary><strong>Q: How do you secure an EC2 instance?</strong></summary>

> Several layers:
> 1. **Security Groups** — allow only required ports; SSH only from specific IPs or a bastion host, never `0.0.0.0/0`
> 2. **Key pairs** — disable password authentication entirely; rotate keys periodically
> 3. **IAM Instance Profile** — attach a role to the EC2 so it can access S3/RDS without hardcoding AWS keys
> 4. **Patching** — run `apt-get update` on a schedule via cron or AWS Systems Manager Patch Manager
> 5. **No public RDS** — database is in a private subnet, only reachable from the EC2's security group
> 
> In Martify, the EC2 instance had an IAM role that allowed `s3:PutObject` for media uploads and `ssm:GetParameter` for secrets — nothing more.

</details>

<details>
<summary><strong>Q: What's the difference between stopping and terminating an EC2 instance?</strong></summary>

> Stopping is like shutting down a PC — the instance stops, you stop paying for compute (but still pay for EBS storage), and you can restart it. The data on the root volume persists. Terminating is permanent deletion — the instance and its root EBS volume are destroyed by default. Elastic IPs and separately-mounted EBS volumes can survive termination if configured. In production, I always attach an Elastic IP so the DNS doesn't change across stop/start cycles.

</details>

---

## 5. AWS S3 — Object Storage

### What It Is

S3 (Simple Storage Service) stores files as objects in buckets. In Django, it replaces the local `MEDIA_ROOT` for user-uploaded files — critical when running multiple EC2 instances, since local storage isn't shared.

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Bucket** | Top-level container; globally unique name |
| **Object** | A file + metadata; key is the full path (`products/iphone.jpg`) |
| **ACL** | Access control — buckets should be private; use pre-signed URLs for access |
| **Versioning** | Keep all versions of an object; enables recovery from accidental deletes |
| **Lifecycle policy** | Auto-archive old objects to S3 Glacier, or delete after N days |
| **Presigned URL** | Time-limited URL that grants temporary access to a private object |

### Django + S3 (django-storages) — Martify Pattern

```python
# settings/production.py
import boto3

# django-storages config
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE  = 'storages.backends.s3boto3.S3StaticStorage'

AWS_STORAGE_BUCKET_NAME = 'martify-media-prod'
AWS_S3_REGION_NAME      = 'ap-south-1'
AWS_S3_FILE_OVERWRITE   = False       # preserve original filenames
AWS_DEFAULT_ACL         = None        # bucket policy handles access, not per-object ACL
AWS_S3_CUSTOM_DOMAIN    = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
```

```python
# utils/s3.py — generating presigned URLs for private assets
import boto3
from botocore.exceptions import ClientError

def generate_presigned_url(bucket: str, key: str, expiry: int = 3600) -> str:
    """
    Returns a pre-signed URL valid for `expiry` seconds.
    Use for private invoices, order receipts, etc.
    """
    s3 = boto3.client('s3', region_name='ap-south-1')
    try:
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=expiry
        )
        return url
    except ClientError as e:
        raise Exception(f"Failed to generate presigned URL: {e}")

# Usage
url = generate_presigned_url('martify-media-prod', 'invoices/order_123.pdf', expiry=600)
```

```python
# Direct upload from Django view
import boto3

def upload_product_image(file_obj, product_id: int) -> str:
    s3 = boto3.client('s3')
    key = f'products/{product_id}/{file_obj.name}'
    s3.upload_fileobj(
        file_obj,
        'martify-media-prod',
        key,
        ExtraArgs={'ContentType': file_obj.content_type}
    )
    return f'https://martify-media-prod.s3.amazonaws.com/{key}'
```

### Interview Q&A

<details>
<summary><strong>Q: Why use S3 instead of storing media files on EC2?</strong></summary>

> EC2 local storage has three problems: it doesn't scale (if you add a second EC2 instance, the second instance doesn't have the files uploaded to the first), it's lost if the instance is terminated, and EBS storage is more expensive per GB than S3. S3 is highly durable (99.999999999%), infinitely scalable, and natively integrates with CloudFront for CDN delivery. With `django-storages`, swapping from local to S3 is a settings change — the `ImageField` and `FileField` work identically from the Django model's perspective.

</details>

<details>
<summary><strong>Q: What is a presigned URL and when do you use it?</strong></summary>

> A presigned URL is a time-limited, signed URL that grants a specific permission (GET or PUT) on a private S3 object without making the object public. You use it when you want your users to access private files directly from S3 (bypassing your server for large downloads) while still controlling access. In Martify, order invoices are stored in a private S3 bucket. When a customer requests their invoice, the Django backend generates a presigned URL valid for 10 minutes and redirects the browser to it — the file is served by S3, not the Django server.

</details>

---

## 6. AWS RDS — Managed Database

### What It Is

RDS (Relational Database Service) is a managed PostgreSQL (or MySQL, etc.) service. "Managed" means AWS handles backups, patching, replication, and failover — you just connect to it like a normal database.

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Instance class** | `db.t3.micro` (dev) → `db.t3.medium` (prod) — CPU/RAM sizing |
| **Multi-AZ** | Synchronous standby in another AZ; automatic failover in ~60s |
| **Read Replica** | Asynchronous copy for read-heavy workloads; Django uses separate DB alias |
| **Parameter Group** | PostgreSQL config (e.g., `max_connections`, `shared_buffers`) |
| **Subnet Group** | Which VPC subnets RDS can use — always private subnets |
| **Automated Backups** | Daily snapshots + transaction logs; point-in-time restore up to 35 days |

### Django Connection to RDS

```python
# settings/production.py
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':     os.environ['RDS_DB_NAME'],       # martify
        'USER':     os.environ['RDS_USERNAME'],       # martify_user
        'PASSWORD': os.environ['RDS_PASSWORD'],       # from SSM Parameter Store
        'HOST':     os.environ['RDS_HOSTNAME'],       # xxx.ap-south-1.rds.amazonaws.com
        'PORT':     '5432',
        'OPTIONS': {
            'connect_timeout': 10,
            'sslmode': 'require',                     # enforce SSL in transit
        },
        'CONN_MAX_AGE': 60,                           # connection pooling: reuse for 60s
    },
    # Optional: read replica for analytics queries
    'read_replica': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ['RDS_READ_REPLICA_HOST'],
        # ... same credentials
    }
}
```

```python
# Using read replica in Django ORM
from django.db import connections

# Router to send read queries to replica
class ReadReplicaRouter:
    READ_MODELS = {'Order', 'Product', 'BlogPost'}

    def db_for_read(self, model, **hints):
        if model.__name__ in self.READ_MODELS:
            return 'read_replica'
        return 'default'

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == 'default'    # only migrate on primary
```

### Interview Q&A

<details>
<summary><strong>Q: What is Multi-AZ and why would you enable it?</strong></summary>

> Multi-AZ keeps a synchronous standby replica of your RDS instance in a different Availability Zone. If the primary fails (hardware fault, AZ outage), RDS automatically promotes the standby and updates the DNS endpoint — no manual intervention, typically under 60 seconds of downtime. The connection string doesn't change because it points to the RDS endpoint (DNS), not a hardcoded IP. For Martify's production database, Multi-AZ is essential because a database outage means no orders can be processed.

</details>

<details>
<summary><strong>Q: How do you connect Django to RDS securely?</strong></summary>

> Three aspects:
> 1. **Network** — RDS is in a private subnet with no public IP; the EC2 and RDS security groups are configured so only the EC2's security group can reach port 5432
> 2. **In-transit encryption** — `sslmode: require` in Django's OPTIONS forces all traffic to be TLS-encrypted
> 3. **Credentials** — DB password is stored in AWS SSM Parameter Store (SecureString), fetched at startup with boto3, never in the codebase or environment files committed to git

</details>

<details>
<summary><strong>Q: How would you handle Django migrations on RDS in a CI/CD pipeline?</strong></summary>

> Migrations are run as a separate step before the new containers start. In the Jenkinsfile, after pulling the new image: `docker run --rm --env-file martify.env martify:latest python manage.py migrate`. This runs as a one-off container and exits. The key constraint is that migrations must be backward-compatible with the currently running version (for zero-downtime deploys), which means: never drop a column in the same release that removes it from the model; instead, do it in a subsequent release.

</details>

---

## 7. AWS IAM — Identity & Access Management

### Core Concepts

| Concept | Description | Example |
|---------|-------------|---------|
| **User** | A person or service with long-term credentials | Jenkins deployer user |
| **Group** | Collection of users sharing a policy | `Developers` group |
| **Role** | Assumed by services/instances temporarily | EC2 instance role |
| **Policy** | JSON document defining allowed/denied actions | Allow `s3:PutObject` on `martify-media/*` |
| **Principle of Least Privilege** | Grant only permissions needed, nothing more | Core IAM philosophy |

### IAM Policy Examples for Martify

```json
// Policy: EC2 can read S3 media bucket and SSM parameters
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "S3MediaAccess",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::martify-media-prod",
                "arn:aws:s3:::martify-media-prod/*"
            ]
        },
        {
            "Sid": "SSMSecretsAccess",
            "Effect": "Allow",
            "Action": [
                "ssm:GetParameter",
                "ssm:GetParameters"
            ],
            "Resource": "arn:aws:ssm:ap-south-1:123456789:parameter/martify/*"
        }
    ]
}
```

```json
// Policy: Jenkins user can push to ECR and deploy to EC2
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ECRAccess",
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:PutImage",
                "ecr:InitiateLayerUpload",
                "ecr:UploadLayerPart",
                "ecr:CompleteLayerUpload"
            ],
            "Resource": "*"
        }
    ]
}
```

### Role vs User — Key Distinction

```
IAM User  → Long-term access keys (AWS_ACCESS_KEY_ID + AWS_SECRET_ACCESS_KEY)
              Used for: CI/CD systems (Jenkins), external tools
              Risk: Keys can be leaked; must be rotated

IAM Role  → Short-term credentials; automatically rotated by AWS
              Used for: EC2 instances, Lambda, ECS tasks
              Best practice: ALWAYS use a role for AWS services, never embed access keys
```

### Interview Q&A

<details>
<summary><strong>Q: What is the difference between an IAM Role and an IAM User?</strong></summary>

> A User has permanent credentials (access key + secret). A Role has no permanent credentials — it is assumed by a trusted entity (EC2 instance, Lambda, another AWS account) and AWS issues short-lived temporary credentials via STS that auto-rotate. For EC2-to-S3 communication in Martify, I attached an IAM Instance Profile (role) to the EC2 — the instance automatically gets rotating credentials. No access key is stored on the server, so there's nothing to leak or rotate manually.

</details>

<details>
<summary><strong>Q: What does least privilege mean and how do you enforce it?</strong></summary>

> Least privilege means granting exactly the permissions an entity needs — no more. In practice: start with no permissions and add only what's required, scope `Resource` ARNs to specific buckets/parameters rather than `*`, use conditions to restrict by IP or time, and audit with IAM Access Analyzer or CloudTrail. For Martify's EC2 role, I restricted S3 access to `martify-media-prod/*` only — the instance can't touch any other bucket even if misconfigured code tries to.

</details>

---

## 8. End-to-End Flow: Martify Deployment

This is how everything connects — the story to tell in an interview when asked about your CI/CD experience.

```
Developer pushes to 'develop' branch on GitHub
        │
        ▼
GitHub webhook triggers Jenkins
        │
        ▼
Jenkins Pipeline starts:
  ├── [Checkout]          git clone onto agent
  ├── [Install deps]      pip install -r requirements.txt
  ├── [Lint]              flake8 checks pass
  ├── [Test]              pytest runs 120 tests → all green, coverage 85%
  ├── [Build Image]       docker build → martify:abc1234
  ├── [Push to ECR]       docker push → AWS ECR private registry
  └── [Deploy Staging]    SSH to EC2 → docker pull + docker run
        │
        ▼
EC2 Staging (t3.small, ap-south-1)
  ├── Pulls image from ECR (IAM Instance Profile handles auth)
  ├── Runs: docker run --env-file martify.env martify:abc1234
  ├── Django reads DB creds from SSM Parameter Store
  └── Connects to RDS PostgreSQL (private subnet, SSL)

        │  (manual QA passes)
        ▼
PR merged to 'main' → Jenkins runs same pipeline
  └── [Deploy Prod] — requires human approval in Jenkins UI
        │
        ▼
EC2 Production (t3.medium, Multi-AZ RDS)
  ├── docker pull martify:abc1234
  ├── docker stop martify_old
  ├── python manage.py migrate   (backward-compatible migration)
  └── docker run martify:abc1234

Media files → S3 (martify-media-prod)
Static files → S3 + CloudFront CDN
```

---

## 9. Quick-Fire Interview Q&A

<details>
<summary><strong>Q: What happens if a Docker container crashes in production?</strong></summary>

> Bare Docker: use `--restart=unless-stopped` flag so Docker daemon auto-restarts the container. Better: use a process supervisor or move to ECS/Fargate where the service definition maintains desired count. In Martify's setup, `docker run --restart=unless-stopped` handled single-node restarts, and CloudWatch alarms monitored EC2 CPU/memory to alert on persistent failures.

</details>

<details>
<summary><strong>Q: How do you roll back a failed deployment?</strong></summary>

> Because every Jenkins build tags the Docker image with the Git SHA, rolling back means running the previous SHA's image. The Jenkins pipeline stores the last good `IMAGE_TAG` as an environment variable. Rollback procedure: SSH to EC2, `docker stop martify`, `docker run <previous-image-tag>`. With ECS, you'd update the task definition to the previous image revision. The key principle: images are immutable and tagged — you never rebuild; you redeploy.

</details>

<details>
<summary><strong>Q: How do you manage database migrations in CI/CD?</strong></summary>

> Migrations run as a separate one-off container before new app containers start. They must be backward-compatible with the old code version that's still running (for zero-downtime). Strategy: (1) deploy migration adding a nullable column, (2) deploy code using the new column, (3) deploy migration removing the old column in a third release. `python manage.py migrate --check` in the Test stage catches if migrations are missing from the commit.

</details>

<details>
<summary><strong>Q: How do you avoid storing AWS credentials in your Dockerfile or code?</strong></summary>

> For EC2: attach an IAM Instance Profile (role) — the instance gets credentials automatically without any keys. For Jenkins: store `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` as Jenkins credentials and inject with `withCredentials`. Never in Dockerfile (image layers are inspectable), never in `.env` files committed to git, never hardcoded. Use `git-secrets` pre-commit hook to block accidental key commits.

</details>

<details>
<summary><strong>Q: What is Docker layer caching and why does it matter in CI?</strong></summary>

> Each instruction in a Dockerfile creates a layer. Docker caches layers and reuses them if nothing above has changed. In CI, if you `COPY requirements.txt` before `COPY . .`, dependencies are only reinstalled when `requirements.txt` changes — not on every code push. For Martify, this cut the Jenkins build time from 4 minutes to 45 seconds because `pip install` was cached on most builds.

</details>

<details>
<summary><strong>Q: What is an ECR and how is it different from Docker Hub?</strong></summary>

> Amazon ECR (Elastic Container Registry) is a private Docker registry hosted in AWS. Unlike Docker Hub (public by default, rate-limited), ECR is private, integrated with IAM (no separate login when using Instance Profiles), and lives in your VPC so image pulls from EC2 don't leave AWS infrastructure. ECR also scans images for known CVEs via ECR Image Scanning. For production Django apps, ECR is preferred because credentials are managed by IAM, not a separate Docker Hub account.

</details>

<details>
<summary><strong>Q: How do you make sure tests don't hit the production database in CI?</strong></summary>

> In the Jenkinsfile, the Test stage sets `DATABASE_URL=sqlite:///test.db` or spins up a temporary Postgres container via `docker-compose -f docker-compose.test.yml`. Django's test runner creates a fresh `test_martify` database, runs tests, then drops it. `pytest-django` with `@pytest.mark.django_db` controls which tests get DB access. No production credentials exist in the Jenkins test environment.

</details>

---

## Cheat Sheet — Key Numbers & Facts

| Topic | Must-Know Fact |
|-------|---------------|
| Docker base image | `python:3.11-slim` not `python:3.11` (saves ~700 MB) |
| RDS failover | Multi-AZ failover in ~60 seconds |
| S3 durability | 99.999999999% (11 nines) |
| Presigned URL | Max expiry: 7 days (for IAM user); 1 hour for Instance Profile |
| IAM | Max 10 managed policies per user/role (soft limit) |
| Jenkins | `Declarative` pipeline (structured) vs `Scripted` pipeline (full Groovy) — prefer Declarative |
| Docker | Default bridge network; containers on same compose file talk by service name |
| EC2 | Instance metadata at `http://169.254.169.254/latest/meta-data/` (internal only) |

---

*Generated for Sami · Martify Domain · Python Backend Interview Prep*
