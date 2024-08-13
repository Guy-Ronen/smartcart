DOCKER_IMAGE ?= smart_cart:local

ifeq ($(shell uname -m), arm64)
	LOCAL_BUILD_FLAGS = --platform linux/amd64
endif

#####
# Help
#####

.PHONY: help
help:
	@echo "Target                          | Description"
	@echo "---------------------------------------------------------------------------------"
	@echo "build                           | Builds the smart_cart image"
	@echo "run                             | Runs the smart_cart and dependency containers"
	@echo "debug                           | Runs the smart_cart and dependency containers"
	@echo "                                | with a configuration that allows pdb breakpoints"
	@echo "shell                           | Runs the smart_cart and database, and enters"
	@echo "                                | a bash prompt in the src directory"
	@echo "test                            | Runs all tests"
	@echo "format                          | Formats the codebase using black and isort"
	@echo "lint                            | Runs static checks"
	@echo "lint-fix                        | Fixes linting errors"
	@echo "generate-jwt                    | Outputs the generated JWT for local API authentication"

#####
# Build
#####
build:
	docker build $(LOCAL_BUILD_FLAGS) -t $(DOCKER_IMAGE) .

#####
# Run
#####
run:
	docker compose up  || docker compose down
	docker compose down

debug:
	docker compose -f docker-compose.yml run --rm --service-ports smart_cart
	docker compose down

shell:
	-docker compose run --rm --service-ports smart_cart bash
	docker compose down

#####
# Test
#####
test:
	-docker compose run --rm smart_cart python -m pytest -vv --cov=smart_cart --cov-report=xml:coverage.xml --cov-report=term
	docker compose down
	python scripts/remove_app_prefix_from_coverage_report.py


#####
# Lint and Format
#####
format:
	docker compose run --rm --no-deps smart_cart black . && isort --check-only .

lint:
	docker compose run --rm --no-deps smart_cart black --check --diff . && flake8 . && isort --check-only . && mypy .

lint-fix:
	docker compose run --rm --no-deps smart_cart black . && isort . && flake8 .

#####
# Scripts
####
generate-jwt:
	docker compose --env-file env_files/local.env run --rm --no-deps smart_cart python scripts/generate_jwt_token.py


#####
# CI targets
#####

ci-lint:
	docker compose run --rm --no-deps smart_cart black --check --diff . && flake8 . && isort --check-only . && mypy .

ci-test:
	docker compose run --rm smart_cart python -m pytest -vv --cov=smart_cart --cov-report=xml:coverage.xml --cov-report=lcov:coverage.lcov --cov-report=term