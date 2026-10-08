#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
if [ ! -f .env ]; then
  echo "Falta .env. Copia .env.example a .env y pon tu token."
  exit 1
fi
exec ./.venv/bin/python bot.py
