#!/bin/zsh -e
# Shutdown if running
docker-compose down
docker-compose -f docker-compose.yml build
docker-compose up
