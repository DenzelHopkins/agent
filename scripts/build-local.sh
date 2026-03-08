#!/bin/sh
# Usage: build-local.sh <env> <image-tag> <context>
# Only builds when env is "local"
ENV=$1
TAG=$2
CONTEXT=$3

if [ "$ENV" != "local" ]; then
  exit 0
fi

nerdctl --namespace k8s.io build -t "$TAG" "$CONTEXT"
