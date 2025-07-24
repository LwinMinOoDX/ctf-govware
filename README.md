# Blogging Website CTF Challenge

This is a Capture The Flag (CTF) challenge designed for deployment on CTFd platform. It involves a multi-container Docker setup with a blogging website, an admin panel, and a logs server.

## Challenge Overview

The challenge consists of three Docker containers:

1. **Blog Server** - A public-facing blogging website with an SSRF vulnerability
2. **Admin Panel** - Only accessible via localhost with a command injection vulnerability
3. **Logs Server** - Contains logs and the flag is in the directory above the logs

## For CTFd Administrators

This challenge is designed to be deployed on CTFd where each participant gets their own isolated instance. See [CTFD_DEPLOYMENT.md](CTFD_DEPLOYMENT.md) for detailed deployment instructions.

### Docker Images Available
- **eddx/ctf-govware-blog:latest** - Blog service with SSRF vulnerability
- **eddx/ctf-govware-admin:latest** - Admin panel with command injection
- **eddx/ctf-govware-logs:latest** - Logs service containing the flag

### Key Features for CTFd
- Individual isolated instances per participant
- Automatic flag generation for each instance
- Multi-container architecture with network isolation
- Nginx reverse proxy for proper routing

## Development/Testing Setup

For development or testing purposes only:

```bash
# Build and start the containers
docker-compose up -d

# Access the applications
# Blog: http://localhost:8080
# Admin Panel: http://localhost:8080/admin (only accessible locally)
```

**Note**: This setup is for development only. For CTF deployment, use CTFd platform with the provided Docker images.

## Challenge Walkthrough

### Step 1: Access the Blog Website

Open your browser and navigate to `http://localhost:8080`. This is the public-facing blog website that anyone can access.

### Step 2: Discover the SSRF Vulnerability

When viewing a blog post, notice that the "Previous Post" and "Next Post" buttons use a vulnerable endpoint `/fetch-next` that accepts a URL parameter. This endpoint has an SSRF (Server-Side Request Forgery) vulnerability.

You can exploit this by modifying the URL to access the admin panel which is only available on localhost:

```
http://localhost:8080/fetch-next?url=http://admin
```

### Step 3: Access the Admin Panel via SSRF

By using the SSRF vulnerability, you can access the admin panel that is otherwise restricted to localhost only. The admin panel has a "View Logs" section.

### Step 4: Exploit the SSRF Vulnerability

First, test the SSRF vulnerability by accessing the admin panel:

```bash
curl "http://localhost:8080/fetch-next?url=http://admin"
```

Note: The SSRF targets the admin container directly (`http://admin`), bypassing the nginx restrictions.

This should return the admin panel HTML, confirming SSRF works.

### Step 5: Chain SSRF with Command Injection

Instead of manually accessing the admin panel through a browser, you can chain the SSRF vulnerability with command injection using curl. The admin panel's "View Logs" endpoint accepts POST requests with a log_file parameter that is vulnerable to command injection.

You can exploit this by using a POST request through the SSRF endpoint:

```bash
curl -X POST "http://localhost:8080/fetch-next?url=http://admin/logs" -d "log_file=admin.log; cat /var/flag/flag.txt" -H "Content-Type: application/x-www-form-urlencoded"
```

Note: The SSRF targets the admin container directly (`http://admin`), not through the nginx proxy.

This will chain the SSRF vulnerability with command injection to directly read the flag.

### Step 6: Capture the Flag

The above command will return a dynamically generated flag in the format: `FLAG{ssrf_cmd_injection_<random_hex>}`

You can also explore the directory structure first:

```bash
curl -X POST "http://localhost:8080/fetch-next?url=http://admin/logs" -d "log_file=admin.log; ls -la /var/flag" -H "Content-Type: application/x-www-form-urlencoded"
```

## Security Architecture Comparison

### Multi-Port Setup Security:
- **Pros**: Clear service separation, easier to configure firewalls per service
- **Cons**: Multiple ports to manage, potential for port scanning
- **Use Case**: Development environments, internal networks

### Single-Port Setup Security:
- **Pros**: Single entry point, centralized access control, rate limiting, easier to manage in production
- **Cons**: More complex configuration, single point of failure
- **Use Case**: Production deployments, public-facing servers

**Key Security Features in Single-Port Setup:**
- Nginx reverse proxy provides additional security layer
- Rate limiting prevents brute force attacks on admin panel
- Centralized logging and monitoring
- Path-based access control instead of port-based

## Vulnerabilities Demonstrated

1. **Server-Side Request Forgery (SSRF)**: The blog application's `/fetch-next` endpoint doesn't validate URLs, allowing attackers to make requests to internal services.

2. **Command Injection**: The admin panel's log viewing functionality executes shell commands without proper input validation.

3. **Network Segmentation Bypass**: Using SSRF to access services that should only be available locally.

4. **Privilege Escalation**: Chaining vulnerabilities to gain access to sensitive information (the flag).

5. **Localhost Restriction Bypass**: Both setups demonstrate how SSRF can bypass localhost-only restrictions.

## Security Concepts Demonstrated

- Network isolation using Docker networks
- Access control (admin panel only accessible via localhost)
- Multi-layered security (logs server only accessible through admin panel)
- The dangers of unvalidated user input in web applications

## Solution Summary

1. Discover the SSRF vulnerability in the blog's pagination feature
2. Use SSRF to access the localhost-only admin panel
3. Exploit command injection in the admin panel's log viewer
4. Use directory traversal to read the flag from the parent directory

## Notes for CTF Creators

This setup demonstrates a realistic scenario with chained vulnerabilities that must be exploited in sequence to capture the flag. It teaches important web security concepts including SSRF, command injection, and the importance of proper input validation.