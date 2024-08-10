DOCKER_IMAGE ?= smart_cart:local

ifeq ($(shell uname -m), arm64)
	LOCAL_BUILD_FLAGS = --platform linux/amd64
endif

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
# CI targets
#####

ci-lint:
	docker compose run --rm --no-deps smart_cart black --check --diff . && flake8 . && isort --check-only . && mypy .

ci-test:
	-docker compose run --rm smart_cart python -m pytest -vv --cov=smart_cart --cov-report=xml:coverage.xml --cov-report=lcov:coverage.lcov --cov-report=term
	docker compose down