#!/bin/bash -e

DOCKER_BUILDKIT=1 docker -l debug build \
    --target cpp-docker-ci \
    -t cpp_ci_env:latest .
