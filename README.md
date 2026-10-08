# zyrexpc-telegram-bot

Telegram bot that controls Docker on the host where it runs. Send commands from your phone, get container output back in chat.

## Features

- List, inspect, start, stop, restart and remove containers
- Read logs, running processes, resource stats, images and disk usage
- Run arbitrary commands inside a container (`/exec`)
- Run `docker compose` actions (`up`, `down`, `ps`, `logs`, `restart`, `pull`, `build`)
- Protection layer: the bot never stops or removes its own container, plus any names you list in `PROTECTED_CONTAINERS`
- Long-poll connection with automatic retry and backoff
- Optional proxy support via `HTTPS_PROXY`
- Optional admin allowlist: if `TELEGRAM_ADMIN_IDS` is empty, everyone can talk to the bot

## Requirements

- Python 3.10+
- Docker CLI available on `PATH` (the bot shells out to `docker`)
- A Telegram bot token from [@BotFather](https://t.me/BotFather)

## Quick start (local)

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt

cp .env.example .env
# edit .env, set TELEGRAM_BOT_TOKEN

./run.sh
```

## Quick start (Docker)

```bash
cp .env.example .env
# edit .env, set TELEGRAM_BOT_TOKEN

docker compose up -d
```

The compose file pulls `ghcr.io/bezyrex/tlgram-bt:latest` and mounts `/var/run/docker.sock` so the bot can manage containers on the host.

## Configuration (`.env`)

| Variable | Required | Description |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | yes | Token from @BotFather |
| `TELEGRAM_ADMIN_IDS` | no | Comma-separated Telegram user IDs. Empty = open to everyone |
| `PROTECTED_CONTAINERS` | no | Comma-separated container names the bot must never stop/remove |
| `HTTPS_PROXY` | no | Proxy URL if Telegram is blocked, e.g. `http://host.docker.internal:7890` |

Build-only variables (`VERSION`, `DOCKERHUB_PROJECT_NAME`, `GHCR_PROJECT_NAME`, ...) are documented in [build/README.md](build/README.md).

## Commands

| Command | Action |
|---|---|
| `/start`, `/help` | Bot info and command list |
| `/ps [filter]` | List containers (`docker ps -a` with optional filter) |
| `/inspect <name>` | Container details |
| `/logs <name> [n]` | Recent logs |
| `/top <name>` | Processes inside container |
| `/exec <name> <command>` | Run command in container |
| `/start_c <name>` | Start container |
| `/stop <name>` | Stop container |
| `/restart <name>` | Restart container |
| `/rm <name>` | Remove container (`-f`) |
| `/stats` | CPU/memory/network usage |
| `/images` | Image list |
| `/pull <image>` | Pull image |
| `/df` | Disk usage |
| `/compose <path> <action>` | `docker compose` in `<path>`; actions: `up\|down\|ps\|logs\|restart\|pull\|build` |
| `/protected` | Show protected container names |

Container names may be abbreviated as long as the prefix matches exactly one container.

## Protection

The bot refuses to stop/remove:

1. Its own container (detected automatically when running inside Docker)
2. Names listed in `PROTECTED_CONTAINERS`
3. Any compose project whose service names collide with the above (for `up`, `down`, `restart`)

## Project layout

```
bot.py           entry point, polling loop, retry/backoff
config.py        .env loader, token, admin IDs, protection config
commands/        Telegram command handlers
events/          error handler
helpers.py       reply chunking (4000 char limit), protection checks
protection.py    protected container resolution
docker_cli.py    docker subprocess wrapper
build/           image build/publish scripts, see build/README.md
compose.yaml     run the published image
Dockerfile       image definition
```

## Development

```bash
./.venv/bin/pip install ruff
./.venv/bin/ruff check .
```

## Building and publishing the image

See [build/README.md](build/README.md).
