#!make

SHELL := /bin/bash

default: build

help:
	@echo "available actions:"
	@echo "    build"
	@echo "        Build container image"
	@echo "    run"
	@echo "        Running the container image"
	@echo '    test'
	@echo '        Run unit tests'

.PHONY: help

build:
	$(call docker_build, ${APP_NAME}-cli, Dockerfile, cli, ${PWD})
	$(call docker_build, ${APP_NAME}-test, Dockerfile, test, ${PWD})

notify:
	$(call docker_run, ${APP_NAME}-cli, ${PWD}, notify -f $(filter-out $@, $(MAKECMDGOALS)))

test:
	$(call docker_run, ${APP_NAME}-test, ${PWD})


DOCKER_BIN = $(shell command -v docker 2> /dev/null)

APP_NAME ?= hermes
BUILD_HASH ?= local
docker_build = DOCKER_BUILDKIT=1 $(DOCKER_BIN) build \
                --tag $(1):$(BUILD_HASH) \
                --file $(2) \
                --target $(3) \
                $(4)

docker_run = $(DOCKER_BIN) run -t --rm \
                -v $(2):/opt/hermes \
                $(1):$(BUILD_HASH) \
                $(3)
