# Secure Credential Management

This document explains how to securely manage device credentials without storing them in plaintext YAML files.

## Quick Start

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your credentials:**
   ```bash
   NORNIR_USERNAME=your_username
   NORNIR_PASSWORD=your_password
   NORNIR_SECRET=your_enable_secret
   ```

3. **Remove credentials from YAML files:**
   - Remove `username:` and `password:` from `conf/hosts.yaml`
   - Remove `username:` and `password:` from `conf/defaults.yaml`
   - Remove `secret:` from `conf/defaults.yaml` and `conf/groups.yaml`

4. **Restart the server** to load the new credentials.

## Environment Variable Options

### Global Defaults (All Devices)

Set these to use the same credentials for all devices:

```bash
NORNIR_USERNAME=admin
NORNIR_PASSWORD=secure_password
NORNIR_SECRET=enable_secret
```

### Per-Host Credentials

Override defaults for specific devices using the device's inventory name:

```bash
# For device named "R1" in hosts.yaml
NORNIR_HOST_R1_USERNAME=admin
NORNIR_HOST_R1_PASSWORD=router1_password
NORNIR_HOST_R1_SECRET=router1_enable

# For device named "SW1" in hosts.yaml
NORNIR_HOST_SW1_USERNAME=admin
NORNIR_HOST_SW1_PASSWORD=switch1_password
```

Or use the device's hostname (replace dots/dashes with underscores):

```bash
# For device with hostname "192.168.1.1"
NORNIR_HOST_192_168_1_1_USERNAME=admin
NORNIR_HOST_192_168_1_1_PASSWORD=device_password
```

## Priority Order

Credentials are loaded in this priority (highest to lowest):

1. **Per-host environment variables** (`NORNIR_HOST_{NAME}_*`)
2. **Values already in YAML files** (if you haven't removed them)
3. **Global environment variables** (`NORNIR_USERNAME`, `NORNIR_PASSWORD`, `NORNIR_SECRET`)

## Docker Deployment

When using Docker, pass environment variables:

### Option 1: Using .env file with docker-compose

1. Create `.env` file in the project root
2. docker-compose will automatically load it

### Option 2: Using docker-compose environment section

Edit `docker-compose.yml`:

```yaml
services:
  nornir-mcp:
    environment:
      - NORNIR_USERNAME=${NORNIR_USERNAME}
      - NORNIR_PASSWORD=${NORNIR_PASSWORD}
      - NORNIR_SECRET=${NORNIR_SECRET}
```

Then set them in your shell or CI/CD system.

### Option 3: Using Docker secrets (Production)

For production, use Docker secrets:

```yaml
services:
  nornir-mcp:
    secrets:
      - nornir_username
      - nornir_password
      - nornir_secret
secrets:
  nornir_username:
    external: true
  nornir_password:
    external: true
  nornir_secret:
    external: true
```

## Alternative: Nornir Secrets Plugins

For enterprise environments, consider using:

- **nornir-salt**: Integrates with HashiCorp Vault, AWS Secrets Manager, etc.
- **nornir-ansible**: Uses Ansible Vault
- **Custom transform functions**: Integrate with your existing secrets management

Example with nornir-salt:

```python
# In nornir_ops.py, modify InitNornir:
from nornir_salt import InventoryFunction

nr = InitNornir(
    config_file=config_file,
    transform_function=InventoryFunction,
    transform_function_options={
        "InventoryFunction": "vault",
        "vault_path": "secret/data/nornir"
    }
)
```

## Security Best Practices

1. ✅ **Never commit `.env` files** - Already in `.gitignore`
2. ✅ **Use different credentials per environment** (dev/staging/prod)
3. ✅ **Rotate credentials regularly**
4. ✅ **Use secrets management systems** (Vault, AWS Secrets Manager) for production
5. ✅ **Restrict file permissions** on `.env` files: `chmod 600 .env`
6. ✅ **Use SSH keys** where possible instead of passwords
7. ✅ **Enable 2FA/MFA** on network devices when available

## Troubleshooting

### Credentials not loading?

1. Check that `.env` file exists and has correct format
2. Verify environment variable names match exactly (case-sensitive)
3. Check server logs for credential loading messages
4. Ensure `python-dotenv` is installed: `pip install python-dotenv`

### Testing credentials

You can test if credentials are loaded by checking the logs when the server starts:
```
[Setup] Using credentials from environment variables
```

If you see this message, environment variables are being used.
