.PHONY: all help push-image bump-version dev-docker

default: help
all: help

help:
	@echo "Usage: make [target]"
	@echo
	@echo "Targets:"
	@echo "  push-image					Push image to registry"
	@echo "  bump-version				Bump version"
	@echo "  dev-docker					Dev docker"
	@echo "  install-dev				Install dev dependencies"


push-image:
	bash dockers/push-image.sh

bump-version:
	bash dockers/bump-version.sh

dev-docker:
	docker compose -f dockers/docker-compose.yml up --build

install-dev:
	pip install -r requirements.txt
