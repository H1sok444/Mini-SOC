# Mini SOC – Wazuh on Docker Swarm (CI/CD)

This repo implements the technical challenge requirements: CI/CD (GitHub Actions), Trivy, Selenium tests, Ansible deploy to Docker Swarm, TLS via Traefik, and custom Wazuh rule/decoder.

## Architecture
- **Docker Swarm**: overlay `wazuh-net`; services: Traefik (TLS), Wazuh Indexer, Manager, Dashboard.
- **CI/CD (GitHub Actions)**:
  - Build images (or pull upstream), Trivy scan (fail on High/Critical).
  - Selenium test: HTTPS reachability + login form.
  - API health probe against dashboard `/api/status`.
  - Deploy to Swarm via Ansible (on `main` only).
- **Secrets**: GitHub Encrypted Secrets → Ansible Vault → Swarm Secrets.
- **TLS**: Traefik + Let’s Encrypt (staging by default) or self-signed fallback.

## Prerequisites (Self-hosted runner)
- Docker & Docker Swarm, Ansible, Python 3.10+, Trivy, Chrome + chromedriver (or Chromium), pytest, selenium.
- Network: open 80/443/1514/1515/55000/9200 on the Swarm ingress node (adjust firewalls accordingly).

## Quickstart (Local)
```bash
# 1) Create overlay and volumes
docker network create -d overlay --attachable wazuh-net || true

# 2) Create acme storage for Traefik
mkdir -p /var/lib/traefik && touch /var/lib/traefik/acme.json && chmod 600 /var/lib/traefik/acme.json

# 3) Deploy
ansible-playbook -i ansible/inventories/production ansible/playbooks/deploy.yml --ask-vault-pass

# 4) Open https://<YOUR_DOMAIN>/  (or https://<MANAGER_IP> with self-signed)
```

## GitHub Secrets to set
- `VAULT_PASSWORD` – password for Ansible Vault.
- `TRAEFIK_EMAIL` – email for Let’s Encrypt.
- `WAZUH_PASSWORD` – dashboard admin password (or set via vault).
- `ANSIBLE_HOST` – Swarm manager SSH host.
- `ANSIBLE_USER` – SSH user.
- `ANSIBLE_SSH_PRIVATE_KEY` – private key for SSH (if not using runner-local SSH agent).

## Rollback
```bash
docker service update --rollback wazuh_traefik
docker service update --rollback wazuh_wazuh-dashboard
docker service update --rollback wazuh_wazuh-manager
docker service update --rollback wazuh_wazuh-indexer
# or
docker stack rm wazuh
```

## Evidence (to produce manually)
- Screenshots of a successful CI run, dashboard login page, Trivy report artifact, and Ansible output.
