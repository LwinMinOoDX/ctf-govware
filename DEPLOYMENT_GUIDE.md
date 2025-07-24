# CTF Govware Deployment Guide

## 🎯 Multi-Container Architecture

This CTF uses a multi-container architecture with Docker Compose for easy deployment and service isolation.

### Services:
- **Blog**: Main web application (port 80)
- **Admin**: Administrative panel (internal access only)
- **Logs**: Log viewing service (internal access only)
- **Nginx**: Reverse proxy and load balancer

### Quick Start:
```bash
git clone https://github.com/LwinMinOoDX/ctf-govware.git
cd ctf-govware
docker-compose up -d
```

### Access:
- **CTF Website**: http://localhost
- **Admin Panel**: Accessible via SSRF vulnerability using `http://admin`
- **Logs Service**: Accessible via SSRF vulnerability using `http://logs`

### SSRF Vulnerability:
The blog application has an SSRF vulnerability that allows access to internal services:
```
http://localhost/fetch-next?url=http://admin
http://localhost/fetch-next?url=http://logs
```

## 🚀 Multi-Container Deployment Options (Original)

### Option 1: Docker Hub + VPS (Recommended)

```bash
# On any server with Docker
wget https://raw.githubusercontent.com/LwinMinOoDX/ctf-govware/main/ctf-govware-distribution/docker-compose.yml
wget https://raw.githubusercontent.com/LwinMinOoDX/ctf-govware/main/ctf-govware-distribution/nginx.conf
docker-compose up -d
```

### Option 2: DigitalOcean App Platform

1. Fork this repository
2. Connect to DigitalOcean App Platform
3. Use the `docker-compose.yml` for deployment

### Option 3: AWS ECS/Fargate

1. Convert `docker-compose.yml` to ECS task definition
2. Deploy using AWS CLI or Console

### Option 4: Google Cloud Run (Multi-container)

```bash
# Deploy each service separately
gcloud run deploy blog --image eddx/ctf-govware-blog:latest
gcloud run deploy admin --image eddx/ctf-govware-admin:latest
gcloud run deploy logs --image eddx/ctf-govware-logs:latest
```

### Option 5: Kubernetes

```bash
# Convert docker-compose to k8s manifests
kompose convert
kubectl apply -f .
```

## 🔧 For Single-Service Platforms (Railway, Render, etc.)

These platforms typically support single containers. You would need to:

1. **Deploy each service separately** on different instances
2. **Configure networking** between services
3. **Set up a reverse proxy** (nginx) on another instance

## 📦 Pre-built Docker Images

All services are available on Docker Hub:
- `eddx/ctf-govware-blog:latest`
- `eddx/ctf-govware-admin:latest`
- `eddx/ctf-govware-logs:latest`

## 🎯 Quick Test Locally

```bash
git clone https://github.com/LwinMinOoDX/ctf-govware.git
cd ctf-govware
docker-compose up -d
# Access at http://localhost:8080
```

## 💡 Alternative: Single Container Approach

If you need Nixpacks compatibility, consider:
1. Combining all services into one container
2. Using process managers like supervisord
3. This would require significant refactoring

---

**Recommendation**: Use a VPS with Docker Compose for the best experience and easiest deployment.