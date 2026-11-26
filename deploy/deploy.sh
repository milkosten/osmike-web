#!/usr/bin/env bash
# Deploy www.osmike.com to 242: rsync the repo to /opt/osmike-web, keep .env, build + up.
set -euo pipefail
H=root@91.98.177.242; K=~/.ssh/mikeos_media
cd "$(dirname "$0")/.."
rsync -az --delete -e "ssh -i $K" --exclude .git --exclude __pycache__ --exclude deploy/.env --exclude plan ./ $H:/opt/osmike-web/
ssh -i $K $H 'mkdir -p /data/osmike-web/contact && chown -R 10001:10001 /data/osmike-web && chmod 700 /data/osmike-web/contact && cd /opt/osmike-web/deploy && test -f .env && docker compose up -d --build 2>&1 | tail -2 && sleep 4 && docker ps --filter name=^osmike-web$ --format "{{.Names}} {{.Status}}"'
