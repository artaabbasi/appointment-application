#!/usr/bin/env bash

cd /home/proj

echo "🧪 Fetching main branch from git "
git fetch
git checkout main
git pull origin main

echo "🧪 Resetting application "
docker-compose down -v --remove-orphans
docker-compose up -d --build

echo "⏳ Waiting for backend-test to become ready..."

until curl -s http://localhost:8000/docs > /dev/null; do
  printf '.'
  sleep 2
done

docker system prune -f