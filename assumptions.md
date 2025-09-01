# Assumptions
- **DNS/Domain**: Assumes a domain is configured for Let’s Encrypt (e.g., `<YOUR_DOMAIN>`) or uses Swarm manager IP for self-signed TLS.
- **TLS**: Let’s Encrypt staging environment used by default; self-signed certificates as fallback. Traefik handles certificate renewal.
- **Runner Permissions**: Self-hosted runner has:
  - Docker and Swarm access
  - Ansible, Python 3.10+, Trivy, Chrome/Chromedriver installed.
  - SSH access to `ANSIBLE_HOST` with `ANSIBLE_USER` and `ANSIBLE_SSH_PRIVATE_KEY`.
- **Network**: Ports 80, 443, 1514, 1515, 55000, 9200 open on Swarm ingress node. Firewall rules allow inbound traffic.
- **Secrets**: GitHub Secrets (`VAULT_PASSWORD`, `TRAEFIK_EMAIL`, etc.) are pre-configured. Ansible Vault password provided at runtime.
- **Environment**: Single-node Swarm for simplicity.
