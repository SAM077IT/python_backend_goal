# AWS Interview Prep — EC2, S3, RDS & IAM
> Tailored to your resume: deploying Django on AWS, S3 for media, RDS for PostgreSQL, IAM for security

---

## Table of Contents
- [EC2 & Deployment](#ec2--deployment)
- [S3 — File Storage](#s3--file-storage)
- [RDS — Managed Database](#rds--managed-database)
- [IAM — Identity & Access Management](#iam--identity--access-management)
- [Other Relevant AWS Services](#other-relevant-aws-services)
- [Scenario-Based Questions](#scenario-based-questions)

---

## EC2 & Deployment

<details>
<summary><strong>1. How do you deploy a Django application on EC2?</strong></summary>

### Answer

**Architecture:**
```
Internet → Route53 (DNS) → ALB (Load Balancer) → EC2 instances → RDS (PostgreSQL)
                                                              ↓
                                                          ElastiCache (Redis)
                                                          S3 (Static/Media)
```

**EC2 setup for Django:**
```bash
# 1. Launch EC2 instance
# - AMI: Ubuntu 22.04 LTS
# - Instance type: t3.medium (2 vCPU, 4GB RAM) for start
# - VPC: Custom VPC with public/private subnets
# - Security Group: port 80, 443 (public), port 22 (your IP only)

# 2. Server setup
sudo apt update && sudo apt upgrade -y
sudo apt install python3.11 python3.11-venv python3-pip nginx supervisor -y

# 3. Application setup
cd /var/www/
git clone https://github.com/yourusername/martify.git
cd martify
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Environment variables
# /etc/environment or .env file (never commit!)
export DATABASE_URL=postgresql://user:pass@rds-endpoint/mydb
export REDIS_URL=redis://elasticache-endpoint:6379/0
export SECRET_KEY=your-django-secret-key
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...

# 5. Collect static files
python manage.py collectstatic --noinput
python manage.py migrate

# 6. Gunicorn config
# /etc/supervisor/conf.d/martify.conf
[program:martify_web]
command=/var/www/martify/venv/bin/gunicorn martify.wsgi:application
    --bind unix:/tmp/martify.sock
    --workers 4
    --worker-class sync
    --timeout 120
    --access-logfile /var/log/martify/access.log
    --error-logfile /var/log/martify/error.log
directory=/var/www/martify
user=www-data
autostart=true
autorestart=true

[program:martify_celery]
command=/var/www/martify/venv/bin/celery
    -A martify worker --loglevel=info --concurrency=4
directory=/var/www/martify
user=www-data
autostart=true
autorestart=true
```

```nginx
# 7. Nginx config
server {
    listen 80;
    server_name martify.com www.martify.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name martify.com www.martify.com;

    ssl_certificate /etc/letsencrypt/live/martify.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/martify.com/privkey.pem;

    client_max_body_size 10M;   # file upload limit

    location /static/ {
        alias /var/www/martify/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        # Redirect to S3 or serve locally
        proxy_pass https://your-bucket.s3.ap-south-1.amazonaws.com/media/;
    }

    location / {
        proxy_pass http://unix:/tmp/martify.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_read_timeout 120s;
    }
}
```

</details>

---

<details>
<summary><strong>2. How do you scale a Django application on EC2?</strong></summary>

### Answer

**Horizontal scaling with Auto Scaling Group:**

```
Route53 → ALB (Application Load Balancer)
              ↓
    Auto Scaling Group (EC2 instances)
    ├── instance-1: Gunicorn (4 workers)
    ├── instance-2: Gunicorn (4 workers)
    └── instance-3: Gunicorn (4 workers)
              ↓
    Shared Resources:
    ├── RDS Multi-AZ (PostgreSQL)
    ├── ElastiCache (Redis — sessions, cache)
    └── S3 (static files, media)
```

**Key requirements for horizontal scaling:**
```python
# 1. Stateless application — sessions in Redis, not memory
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# 2. Shared cache — Redis (not in-memory)
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://elasticache-cluster.abc.cache.amazonaws.com:6379/0',
    }
}

# 3. Shared file storage — S3 (not local disk)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

# 4. Shared task queue — Celery with Redis broker
CELERY_BROKER_URL = 'redis://elasticache-cluster:6379/1'

# Auto Scaling policy (AWS Console or Terraform)
# Scale out: add instance when CPU > 70% for 2 minutes
# Scale in: remove instance when CPU < 30% for 10 minutes
# Min instances: 2 (for high availability)
# Max instances: 10
```

**Gunicorn worker count formula:**
```bash
# workers = (2 × number_of_CPU_cores) + 1
# t3.medium: 2 cores → 5 workers
gunicorn martify.wsgi:application --workers 5

# For async (async views): use uvicorn workers
gunicorn martify.asgi:application -k uvicorn.workers.UvicornWorker --workers 5
```

</details>

---

## S3 — File Storage

<details>
<summary><strong>3. How do you integrate S3 with Django for media and static files?</strong></summary>

### Answer

```python
# pip install boto3 django-storages

# settings.py
import boto3

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_S3_BUCKET_NAME')
AWS_S3_REGION_NAME = 'ap-south-1'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# S3 settings
AWS_DEFAULT_ACL = None              # use bucket policy, not object ACL
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',   # cache 1 day
}
AWS_QUERYSTRING_AUTH = True        # private files require signed URL
AWS_QUERYSTRING_EXPIRE = 3600      # signed URLs expire in 1 hour

# Static files (public)
STATICFILES_STORAGE = 'myapp.storage.StaticStorage'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'

# Media files (private)
DEFAULT_FILE_STORAGE = 'myapp.storage.MediaStorage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# custom storage backends
# myapp/storage.py
from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'

class MediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = None        # private
    file_overwrite = False    # never overwrite — unique filename

class PrivateMediaStorage(S3Boto3Storage):
    location = 'private'
    default_acl = None
    custom_domain = False     # don't expose direct URL

# Usage in views — generate pre-signed URL for private files
import boto3

def get_signed_url(s3_key: str, expires_in: int = 3600) -> str:
    """Generate temporary access URL for private S3 files."""
    s3_client = boto3.client(
        's3',
        region_name='ap-south-1',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    return s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': s3_key,
        },
        ExpiresIn=expires_in
    )

# Upload directly to S3 from view
def upload_product_image(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    file = request.FILES.get('image')

    if not file:
        return Response({"error": "No file provided"}, status=400)

    # Validate file
    validate_upload(file)

    # Save to S3 via model field (django-storages handles the upload)
    product.image = file
    product.save(update_fields=['image'])

    return Response({"image_url": product.image.url})

# Pre-signed POST URL — upload from client directly to S3
def get_upload_url(request):
    """Let client upload directly to S3 — reduces server load."""
    s3_client = boto3.client('s3', region_name='ap-south-1')
    filename = f"uploads/{request.user.id}/{uuid.uuid4()}.jpg"

    presigned = s3_client.generate_presigned_post(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=filename,
        Fields={"Content-Type": "image/jpeg"},
        Conditions=[
            {"Content-Type": "image/jpeg"},
            ["content-length-range", 1, 5 * 1024 * 1024],   # 1 byte to 5MB
        ],
        ExpiresIn=300   # 5 minutes to use this URL
    )
    return Response({"upload_url": presigned['url'], "fields": presigned['fields']})
```

</details>

---

<details>
<summary><strong>4. What is an S3 bucket policy vs ACL? How do you secure your S3 buckets?</strong></summary>

### Answer

```json
// Bucket Policy — resource-based policy (recommended over ACLs)
// More powerful, can reference IAM roles, IPs, VPCs
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowStaticFiles",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::martify-static/*"
        },
        {
            "Sid": "DenyNonHTTPS",
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:*",
            "Resource": "arn:aws:s3:::martify-media/*",
            "Condition": {
                "Bool": {"aws:SecureTransport": "false"}
            }
        },
        {
            "Sid": "RestrictToApplication",
            "Effect": "Allow",
            "Principal": {"AWS": "arn:aws:iam::ACCOUNT_ID:role/MartifyEC2Role"},
            "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
            "Resource": "arn:aws:s3:::martify-media/*"
        }
    ]
}
```

```python
# S3 security checklist:

# 1. Block Public Access (always enable unless bucket is intentionally public)
# AWS Console: S3 → Bucket → Permissions → Block all public access → ON

# 2. Separate buckets by sensitivity
# martify-static → public (CloudFront CDN)
# martify-media  → private (signed URLs only)
# martify-backups → private + versioning + MFA delete

# 3. Enable versioning + lifecycle
# Protects against accidental deletion

# 4. Enable server-side encryption
AWS_S3_OBJECT_PARAMETERS = {
    'ServerSideEncryption': 'AES256',  # or 'aws:kms' for KMS
}

# 5. Enable access logging
# S3 → Bucket → Properties → Server access logging

# 6. Use CloudFront for static files (faster + extra security layer)
STATIC_URL = 'https://d1234abcd.cloudfront.net/static/'
```

</details>

---

## RDS — Managed Database

<details>
<summary><strong>5. Why use RDS instead of self-managed PostgreSQL on EC2?</strong></summary>

### Answer

| Feature | RDS | Self-managed on EC2 |
|---|---|---|
| **Automated backups** | Built-in, point-in-time recovery | Manual setup |
| **Multi-AZ failover** | Automatic (1-2 min) | Manual setup |
| **Read replicas** | 1-click | Manual replication setup |
| **Patching** | Automated | Manual |
| **Monitoring** | CloudWatch + Enhanced Monitoring | Manual setup |
| **Storage scaling** | Auto Storage Scaling | Manual |
| **Cost** | Higher | Lower (but ops overhead) |
| **Control** | Less | More |

```python
# Django config for RDS
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=env('DATABASE_URL'),
        conn_max_age=60,
        conn_health_checks=True,   # verify connection health before reuse
    )
}

# DATABASE_URL format:
# postgresql://user:password@rds-endpoint.ap-south-1.rds.amazonaws.com:5432/martifydb

# RDS best practices:
# 1. Use private subnet — not publicly accessible
# 2. Security group: only EC2 security group can connect on port 5432
# 3. Enable Multi-AZ for production (automatic failover)
# 4. Set up read replica for heavy read workloads
# 5. Enable automatic minor version upgrades
# 6. Set backup retention: 7-30 days
# 7. Enable Performance Insights for query analysis

# Read replica for analytics
DATABASES = {
    'default': {   # write database
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': env('RDS_WRITE_HOST'),
    },
    'replica': {   # read replica
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': env('RDS_READ_HOST'),
        'TEST': {'MIRROR': 'default'},   # tests use default DB
    }
}

# Database router
class PrimaryReplicaRouter:
    def db_for_read(self, model, **hints):
        """Send reads to replica."""
        return 'replica'

    def db_for_write(self, model, **hints):
        """Send writes to primary."""
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == 'default'   # only run migrations on primary

DATABASE_ROUTERS = ['myapp.routers.PrimaryReplicaRouter']
```

</details>

---

## IAM — Identity & Access Management

<details>
<summary><strong>6. How do you implement least-privilege IAM in your application?</strong></summary>

### Answer

**Principle of Least Privilege — give only the permissions actually needed.**

```json
// IAM Policy for your Django application (EC2 role)
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "S3MediaAccess",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Resource": "arn:aws:s3:::martify-media/*"
        },
        {
            "Sid": "S3StaticRead",
            "Effect": "Allow",
            "Action": ["s3:GetObject"],
            "Resource": "arn:aws:s3:::martify-static/*"
        },
        {
            "Sid": "SESSendEmail",
            "Effect": "Allow",
            "Action": [
                "ses:SendEmail",
                "ses:SendRawEmail"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "ses:FromAddress": "noreply@martify.com"
                }
            }
        },
        {
            "Sid": "SecretsManagerAccess",
            "Effect": "Allow",
            "Action": ["secretsmanager:GetSecretValue"],
            "Resource": "arn:aws:secretsmanager:ap-south-1:ACCOUNT:secret:prod/martify/*"
        },
        {
            "Sid": "CloudWatchLogs",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:ap-south-1:ACCOUNT:log-group:/martify/*"
        }
    ]
}
```

```python
# IAM best practices in your application:

# 1. Use IAM Roles for EC2, NOT access keys
# EC2 instance has a role attached → boto3 uses role credentials automatically
# No keys in environment or code!

import boto3
# boto3 automatically uses EC2 instance role
s3 = boto3.client('s3')  # no credentials needed!

# 2. Use IAM Roles for developers (not root or shared accounts)
# Dev: ReadOnly + specific write permissions to dev environment
# DevOps: Deploy permissions to production
# Admin: Full access (MFA required)

# 3. Rotate credentials regularly
# For any long-lived credentials (legacy), use AWS Secrets Manager rotation

# 4. Environment-based separation
# IAM condition: only allow access to prod resources from prod account
{
    "Condition": {
        "StringEquals": {
            "aws:ResourceTag/Environment": "production"
        }
    }
}

# 5. Monitoring — CloudTrail for all IAM and API activity
# AWS Config for compliance checks
# GuardDuty for threat detection
```

</details>

---

## Other Relevant AWS Services

<details>
<summary><strong>7. Which other AWS services would you use to complement your Django backend?</strong></summary>

### Answer

```python
# AWS SES — sending emails (from your Martify project)
import boto3

class AWSEmailService:
    def __init__(self):
        self.client = boto3.client('ses', region_name='ap-south-1')

    def send(self, to: list, subject: str, html_body: str, text_body: str = ''):
        response = self.client.send_email(
            Source='Martify <noreply@martify.com>',
            Destination={'ToAddresses': to},
            Message={
                'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                'Body': {
                    'Html': {'Data': html_body, 'Charset': 'UTF-8'},
                    'Text': {'Data': text_body, 'Charset': 'UTF-8'},
                }
            }
        )
        return response['MessageId']

# AWS ElastiCache (Redis) — managed Redis for Django cache + Celery
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://martify.abc123.ng.0001.aps1.cache.amazonaws.com:6379/0',
    }
}
CELERY_BROKER_URL = 'redis://martify.abc123.ng.0001.aps1.cache.amazonaws.com:6379/1'

# AWS CloudFront — CDN for static files
STATIC_URL = 'https://d1234abcdef.cloudfront.net/static/'

# AWS CloudWatch — monitoring + alerting
import boto3

cloudwatch = boto3.client('cloudwatch', region_name='ap-south-1')

def put_custom_metric(metric_name: str, value: float, unit: str = 'Count'):
    cloudwatch.put_metric_data(
        Namespace='Martify/Application',
        MetricData=[{
            'MetricName': metric_name,
            'Value': value,
            'Unit': unit,
        }]
    )

# Usage
put_custom_metric('OrdersPlaced', 1)
put_custom_metric('PaymentErrors', 1)

# Django middleware to send metrics
class CloudWatchMetricsMiddleware:
    def __call__(self, request):
        start = time.perf_counter()
        response = self.get_response(request)
        duration = time.perf_counter() - start

        put_custom_metric('ResponseTime', duration * 1000, 'Milliseconds')
        if response.status_code >= 500:
            put_custom_metric('5xxErrors', 1)

        return response

# AWS Secrets Manager — secure credential storage
def get_db_credentials():
    client = boto3.client('secretsmanager', region_name='ap-south-1')
    secret = client.get_secret_value(SecretId='prod/martify/database')
    return json.loads(secret['SecretString'])

# AWS SQS — alternative to Redis for Celery (more durable)
CELERY_BROKER_URL = 'sqs://'
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'region': 'ap-south-1',
    'visibility_timeout': 3600,
    'polling_interval': 1,
}
```

</details>

---

## Scenario-Based Questions

<details>
<summary><strong>8. Your production server on EC2 is under heavy load — what steps do you take?</strong></summary>

### Answer

```
Immediate (0-5 min):
1. Check CloudWatch metrics — CPU, memory, network, disk I/O
2. Check application logs — are there errors? Which endpoint is slow?
3. Check active connections to RDS — is DB overwhelmed?
4. Check Redis memory and connection count

Short-term (5-30 min):
5. Enable CloudFront caching if not already
6. Increase Gunicorn workers (if CPU bound) or add more EC2 instances
7. Identify and kill runaway queries in PostgreSQL
8. Enable Django cache for expensive views

Long-term:
9. Add Auto Scaling Group with proper scaling policies
10. Add read replica for read-heavy queries
11. Move heavy tasks to Celery workers
12. Add CDN for static assets
13. Consider ElastiCache for session and view caching
```

```python
# Quick performance wins in Django under load

# 1. Enable aggressive caching
@cache_page(60 * 5)   # 5 min cache for product listings
def product_list(request):
    ...

# 2. Defer heavy computation to Celery
def generate_report(request):
    task = generate_report_task.delay(request.user.id)
    return Response({"task_id": str(task.id), "status": "processing"})

# 3. Reduce DB query count
# Before: 150 queries for order list
# After: 3 queries (select_related + prefetch_related)

# 4. Use .values() for read-only list endpoints
def product_list_api(request):
    products = Product.active.values(
        'id', 'name', 'price', 'stock', 'category__name'
    ).order_by('-created_at')
    return JsonResponse(list(products), safe=False)

# 5. Add database connection pooling
DATABASES['default']['CONN_MAX_AGE'] = 60
```

</details>

