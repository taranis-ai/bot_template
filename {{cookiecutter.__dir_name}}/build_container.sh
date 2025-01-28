#!/bin/bash

if [ ! -e "uv.lock" ]
then
    echo "uv.lock does not exist. Please run uv sync to create it"
    echo "Error: Cannot build container without uv.lock -> Abort"
    exit
fi

set -eou pipefail

cd $(git rev-parse --show-toplevel)

GITHUB_REPOSITORY_OWNER=${GITHUB_REPOSITORY_OWNER:-"ghcr.io/taranis-ai"}
buildx_tags="--tag ${GITHUB_REPOSITORY_OWNER}/taranis-awesomebot:latest "

if git rev-parse --quiet --verify HEAD >/dev/null; then
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD | sed 's/[^a-zA-Z0-9_.-]/_/g')
    echo "Building image for branch ${CURRENT_BRANCH} on ${GITHUB_REPOSITORY_OWNER}"
    buildx_tags+="--tag ${GITHUB_REPOSITORY_OWNER}/taranis-awesomebot:${CURRENT_BRANCH}"
else
    echo "The repository has no commits yet. Building image locally"
fi


docker buildx build --file Containerfile \
  --build-arg GITHUB_REPOSITORY_OWNER="${GITHUB_REPOSITORY_OWNER}" \
  $buildx_tags \
  --load .
