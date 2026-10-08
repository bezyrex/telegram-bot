#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
if [ ! -f .env ]; then
  echo "You need to copy .env.example to .env, and fill the variables."
  exit 1
fi
exec ./.venv/bin/python bot.py
