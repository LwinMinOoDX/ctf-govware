# CTF Govware Deployment Guide

## 🎯 Nixpacks Solution (Single Container)

**✅ FIXED!** This repository now includes a `Dockerfile.single` and `nixpacks.toml` that makes it compatible with Nixpacks-based platforms like Railway, Render, and others.

### For Nixpacks Platforms (Railway, Render, etc.):

1. **Push to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Add Nixpacks support"
   git push origin main
   ```

2. **Deploy on Railway**:
   - Connect your GitHub repository
   - Railway will automatically detect `nixpacks.toml`
   - The app will build using `Dockerfile.single`
   - Access your CTF at the provided Railway URL

3. **Deploy on Render**:
   - Connect your GitHub repository
   - Render will use the Nixpacks configuration
   - Access your CTF at the provided Render URL

### Quick Deploy with DockerHub:
Alternatively, you can deploy the pre-built image directly:
```bash
docker run -p 80:80 eddx/ctf-govware-single:latest
```

### How the Single Container Works:
- All services (blog, admin, logs) run on different ports (5000, 5001, 5002)
- Nginx reverse proxy routes traffic appropriately
- Supervisor manages all processes in one container
- SSRF vulnerability: Use `http://localhost:5001` to access admin
- Admin panel accessible at `/admin` path

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