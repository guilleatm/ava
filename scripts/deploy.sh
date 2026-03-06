#!/bin/bash

cd ~/ava/

DOCKER_BUILDKIT=0 docker compose down

git add .
git stash
git pull
git stash pop

DOCKER_BUILDKIT=0 docker compose -p asterisk-ai-voice-agent up -d --build --force-recreate admin_ui