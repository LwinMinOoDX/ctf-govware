# CTFd Deployment Guide

## Overview

This CTF challenge is designed to be deployed on CTFd platform where each participant gets their own isolated instance. The challenge uses Docker images hosted on Docker Hub that CTFd can automatically deploy for individual users.

## Docker Images for CTFd

The following Docker images are available on Docker Hub for CTFd deployment:

- **eddx/ctf-govware-blog:latest** - Blog service with SSRF vulnerability
- **eddx/ctf-govware-admin:latest** - Admin panel with command injection
- **eddx/ctf-govware-logs:latest** - Logs service containing the flag

## CTFd Configuration

### Challenge Type
- **Type**: Dynamic Challenge
- **Category**: Web Security
- **Points**: 500 (suggested)
- **Max Attempts**: Unlimited

### Docker Configuration for CTFd

#### Network Setup
CTFd should create isolated networks for each instance:
```yaml
networks:
  blog_network:
    driver: bridge
  admin_logs_network:
    driver: bridge
```

#### Service Configuration
```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"  # CTFd will assign random external port
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - blog
      - admin
    networks:
      - blog_network

  blog:
    image: eddx/ctf-govware-blog:latest
    networks:
      - blog_network
      - admin_logs_network

  admin:
    image: eddx/ctf-govware-admin:latest
    networks:
      - admin_logs_network
      - blog_network

  logs:
    image: eddx/ctf-govware-logs:latest
    networks:
      - admin_logs_network
```

### Required Files for CTFd

1. **docker-compose.yml** - Service configuration
2. **nginx.conf** - Nginx routing configuration

### CTFd Instance Benefits

✅ **Isolated Environments**: Each participant gets their own instance
✅ **No Interference**: Users can't affect each other's progress
✅ **Automatic Cleanup**: CTFd handles container lifecycle
✅ **Scalable**: Can handle multiple concurrent users
✅ **Unique Flags**: Each instance generates its own flag

## Challenge Description for CTFd

### Title
"Multi-Service Web Exploitation"

### Description
```
You've discovered a blogging website that seems to have some interesting features. 
The site appears to be running multiple services behind a reverse proxy.

Your goal is to find and exploit vulnerabilities to access restricted areas and capture the flag.

Hints:
- Look for ways to make the server request internal resources
- Admin panels often have interesting functionality
- Sometimes you need to chain multiple vulnerabilities together

Access your instance at: {instance_url}

Flag format: FLAG{ssrf_cmd_injection_*}
```

### Solution Overview
1. Discover SSRF vulnerability in blog pagination
2. Use SSRF to access localhost-only admin panel
3. Exploit command injection in admin log viewer
4. Chain vulnerabilities to read the flag

## Technical Requirements

### CTFd Platform Requirements
- Docker support enabled
- Dynamic challenge plugin
- Sufficient resources for multi-container instances

### Resource Allocation (per instance)
- **CPU**: 0.5 cores
- **Memory**: 512MB
- **Storage**: 1GB
- **Network**: Isolated bridge network

## Deployment Steps for CTFd Admin

1. **Upload Challenge Files**
   - Upload `docker-compose.yml` and `nginx.conf` to CTFd
   
2. **Configure Challenge**
   - Set challenge type to "Dynamic"
   - Configure Docker settings
   - Set resource limits
   
3. **Test Instance**
   - Deploy test instance
   - Verify all services are accessible
   - Confirm vulnerabilities work as expected
   
4. **Publish Challenge**
   - Make challenge available to participants
   - Monitor resource usage

## Monitoring and Maintenance

### Health Checks
- Blog service responds on port 80
- Admin panel accessible via SSRF
- Flag generation working correctly

### Common Issues
- **Port conflicts**: CTFd handles port assignment
- **Network isolation**: Ensure proper network configuration
- **Resource limits**: Monitor CPU/memory usage

## Security Considerations

### Intentional Vulnerabilities
- SSRF in blog pagination feature
- Command injection in admin log viewer
- Network access between containers

### Security Measures
- Containers run with limited privileges
- No persistent data storage
- Isolated networks per instance
- Automatic cleanup after challenge completion

## Support Information

**Challenge Author**: [Your Name]
**Docker Images**: Available on Docker Hub (eddx/ctf-govware-*)
**Estimated Solve Time**: 30-60 minutes
**Difficulty**: Intermediate

For technical support or questions about deployment, contact the challenge author.