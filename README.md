# Novamira — fresh WordPress test environment

A clean WordPress install (Docker Compose) for developing and testing the **Novamira** plugin.

## Stack
- WordPress (`wordpress:php8.3-apache`) on http://localhost:8080
- MySQL 8.4
- WP-CLI (one-shot, via the `cli` profile)
- Novamira plugin mounted live from `./plugins/novamira`

## Quick start

```bash
# 1. Bring it up
docker compose up -d

# 2. Watch WP become ready (first boot copies core into the volume)
docker compose logs -f wordpress

# 3. Open the installer
open http://localhost:8080
```

Finish the famous 5-minute install in the browser, then activate **Novamira**
under Plugins. Because the plugin is bind-mounted, edits to
`plugins/novamira/*.php` are reflected immediately — no rebuild.

## Optional: scripted install with WP-CLI

```bash
docker compose run --rm wpcli core install \
  --url=http://localhost:8080 \
  --title="Novamira Dev" \
  --admin_user=admin \
  --admin_password=admin \
  --admin_email=ben.c.merrell@gmail.com

docker compose run --rm wpcli plugin activate novamira
```

## Manage

```bash
docker compose down          # stop, keep data
docker compose down -v       # stop and WIPE the WP + DB volumes (fresh start)
```

## Files
- `docker-compose.yml` — services
- `.env` — generated DB credentials (gitignored)
- `plugins/novamira/` — the plugin under test
