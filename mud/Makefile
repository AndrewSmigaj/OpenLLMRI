# Whiteout MUD — developer entry points. Everything runs through Docker.
# The torch bot-agent is the one exception: it runs on the host (see agent/).
# The host-fast gates (lint, test-host) also run without Docker, for a tight inner loop.

SCENARIO ?= smoketest
DC = docker compose

.PHONY: help build init migrate accounts up up-d down restart logs \
        load-scenario test test-host lint bake fuzz test-int validate verify \
        reset-db shell agent

help:
	@echo "Whiteout MUD make targets:"
	@echo "  build          build the evennia image"
	@echo "  init           scaffold the Evennia game dir (one-time)"
	@echo "  migrate        run DB migrations against Postgres"
	@echo "  accounts       create admin + bot accounts (idempotent)"
	@echo "  up / up-d      run the server (foreground / detached)"
	@echo "  down           stop the stack"
	@echo "  restart        reload the running server"
	@echo "  logs           follow the evennia logs"
	@echo "  load-scenario  load a scenario (SCENARIO=smoketest)"
	@echo "  test           run the pure sim/ unit tests in Docker (no DB)"
	@echo "  test-host      run the pure tests + gates on the HOST (no Docker; fast loop)"
	@echo "  lint           run the pure-core boundary/determinism + no-raw-writes gates (host)"
	@echo "  test-int       run the Evennia integration tests"
	@echo "  validate       run the content-lint (SCENARIO=smoketest)"
	@echo "  bake           compile authored scenario sources to baked runtime data"
	@echo "  fuzz           run the solvability-fuzz harness"
	@echo "  verify         gates + compose config check + tests"
	@echo "  reset-db       DESTROY the Postgres volume and start fresh"
	@echo "  shell          open an Evennia/Django shell"
	@echo "  agent          run the scripted bot against the running server"

build:
	$(DC) build

# One-time scaffold. Uses `docker run` (not compose) so the ./game:/usr/src/game
# volume isn't auto-created empty first (which would make `--init game` refuse).
# Mounts the repo root at /host and creates ./game there.
init:
	docker run --rm -v "$(CURDIR)":/host -w /host --entrypoint evennia whiteout-evennia:latest --init game

migrate:
	$(DC) run --rm evennia evennia migrate

# Superuser (Account #1) is created over a pty (Evennia's non-TTY createsuperuser
# loops forever); needs host python + pexpect (`pip install pexpect`). The bot
# account is then created via the shell, which works once Account #1 exists.
accounts:
	python3 scripts/create_superuser.py
	cat scripts/bootstrap_accounts.py | $(DC) run --rm -T --entrypoint evennia evennia shell

up:
	$(DC) up

up-d:
	$(DC) up -d

down:
	$(DC) down

restart:
	$(DC) run --rm evennia evennia reload || $(DC) restart evennia

logs:
	$(DC) logs -f evennia

# NOTE: the engine, scenarios and bot harness aren't built yet (see
# docs/scenarios/whiteout/roadmap.md). These targets are the intended dev
# interface; they degrade gracefully until there's something to run.

# Loads a scenario once one exists. When you author world/scenarios/<name>/build.py,
# the loader call below becomes live (it's the documented invocation).
load-scenario:
	@echo "No scenarios built yet (SCENARIO=$(SCENARIO))."
	@echo "See docs/guides/adding-a-scenario.md and game/world/scenarios/README.md."
	@echo "Once built, this runs: evennia shell -c 'from world.scenarios.$(SCENARIO).build import build; build()'"

# Pure unit tests: no Postgres, no Evennia boot. Tolerates 'no tests collected' (exit 5).
test:
	@$(DC) run --rm --no-deps evennia pytest -q tests/sim; ec=$$?; \
	if [ $$ec -eq 5 ]; then echo "(no sim tests yet — see game/tests/README.md)"; else exit $$ec; fi

# Host-fast gates (no Docker, stdlib only): the functional-core boundary/determinism
# gate and the no-raw-writes gate (DR-10/DR-12). Milliseconds; safe to run constantly.
lint:
	python3 tools/lints/check_pure_core.py
	python3 tools/lints/check_no_raw_writes.py

# Host-fast pure tests + gates (no Docker). The full pure suite also runs in Docker
# via `make test`; this is the tight inner loop when host python has pytest.
test-host: lint
	@if PYTHONPATH=game python3 -c "import pytest" >/dev/null 2>&1; then \
	  PYTHONPATH=game python3 -m pytest -q -p no:django game/tests/sim; ec=$$?; \
	  if [ $$ec -eq 5 ]; then echo "(no sim tests yet — see game/tests/README.md)"; else exit $$ec; fi; \
	else echo "host pytest not installed — gates passed; run 'make test' for the full pure suite in Docker"; fi

# Build-time tools (offline; never runtime).
bake:
	python3 tools/bake.py $(SCENARIO)

fuzz:
	python3 tools/fuzz.py $(SCENARIO)

# Integration tests run through Evennia's own test runner (needs a test DB).
test-int:
	@echo "No integration tests yet (see game/tests/README.md)."
	@echo "Once written, this runs: evennia test --settings settings tests.integration"

validate:
	@echo "Content validation lands with the engine (design §44)."
	@echo "See docs/guides/validation-rules.md and game/world/sim/README.md."

verify: lint
	$(DC) config -q
	$(MAKE) test
	@echo "verify: gates + compose config OK + tests run. (validate is engine-stage; roadmap.)"

reset-db:
	$(DC) down -v

shell:
	$(DC) run --rm evennia evennia shell

# The bot harness isn't built yet (only the brain interface exists).
agent:
	@echo "Bot harness not built yet — only the interface exists (agent/brains/base.py)."
	@echo "See agent/README.md for the plan."
