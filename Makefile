# Bitcoin Drill: one-stop commands.  Run `make help`.
REPO ?= $(HOME)/bitcoin-journal
PORT ?= 8000
PY   ?= python3
PUSH ?= 1
EX   ?= 01
L    ?= python
PUSHFLAG := $(if $(filter 1,$(PUSH)),--push)

.DEFAULT_GOAL := help
.PHONY: help setup free-port run start stop restart status logs streak sync update push reset ex-start ex-check clean

help:
	@echo "Bitcoin Drill (REPO=$(REPO) PORT=$(PORT) PUSH=$(PUSH))"
	@echo ""
	@echo "  make setup              create/check the journal repo"
	@echo "  make run                free the port, run in foreground (Ctrl+C stops)"
	@echo "  make start              free the port, run in background"
	@echo "  make stop | restart     stop / restart the background server"
	@echo "  make status | logs      is it up? streak, or tail the log"
	@echo "  make streak             print your GitHub-style commit streak"
	@echo "  make sync               pull --rebase then push your repo"
	@echo "  make push               push your repo"
	@echo "  make reset              erase quiz progress (answer history kept)"
	@echo "  make ex-start EX=01 L=go    copy exercise into repo in one language"
	@echo "  make ex-check EX=01 L=go    run tests, commit only if green"
	@echo "  make clean              remove pid/log/cache files"
	@echo ""
	@echo "Override anything: make start REPO=~/my-repo PORT=9000 PUSH=0"
	@echo "Languages for L: python go rust cpp js"

setup:
	@command -v $(PY) >/dev/null || { echo "python3 not found"; exit 1; }
	@command -v git >/dev/null || { echo "git not found"; exit 1; }
	@if [ ! -d "$(REPO)/.git" ]; then mkdir -p "$(REPO)" && git -C "$(REPO)" init -q && echo "Created new git repo at $(REPO)"; fi
	@git -C "$(REPO)" remote -v | grep . || echo "No remote yet. Run: git -C $(REPO) remote add origin git@github.com:YOU/bitcoin-journal.git"
	@echo "user.email: $$(git config user.email || echo NOT SET)  (must be an email on your GitHub account)"

free-port:
	@pids=$$(lsof -ti tcp:$(PORT) 2>/dev/null || true); \
	if [ -z "$$pids" ] && command -v fuser >/dev/null 2>&1; then pids=$$(fuser $(PORT)/tcp 2>/dev/null || true); fi; \
	if [ -z "$$pids" ] && command -v ss >/dev/null 2>&1; then pids=$$(ss -ltnp "sport = :$(PORT)" 2>/dev/null | grep -o 'pid=[0-9]*' | cut -d= -f2 | sort -u); fi; \
	if [ -n "$$pids" ]; then echo "Port $(PORT) busy, killing: $$pids"; kill $$pids 2>/dev/null; sleep 1; kill -9 $$pids 2>/dev/null || true; else echo "Port $(PORT) is free"; fi

run: setup free-port
	@echo "Open http://localhost:$(PORT)"
	@$(PY) server.py --repo "$(REPO)" --port $(PORT) $(PUSHFLAG)

start: setup free-port
	@nohup $(PY) server.py --repo "$(REPO)" --port $(PORT) $(PUSHFLAG) > .server.log 2>&1 & echo $$! > .server.pid
	@sleep 1; if kill -0 $$(cat .server.pid) 2>/dev/null; then echo "Running at http://localhost:$(PORT) (log: .server.log)"; else echo "Failed to start:"; cat .server.log; exit 1; fi

stop:
	@if [ -f .server.pid ]; then kill $$(cat .server.pid) 2>/dev/null || true; rm -f .server.pid; fi
	@$(MAKE) --no-print-directory free-port

restart: stop start

status:
	@$(PY) -c "import urllib.request as u;print('Running. ' + u.urlopen('http://localhost:$(PORT)/api/streak',timeout=2).read().decode())" 2>/dev/null || echo "Not running on port $(PORT)"

logs:
	@tail -n 40 .server.log

streak: status

sync:
	@git -C "$(REPO)" pull --rebase --autostash && git -C "$(REPO)" push

update: sync

push:
	@git -C "$(REPO)" push

reset:
	@printf "Erase quiz progress in $(REPO)? Answer history is kept. [y/N] "; read a; [ "$$a" = y ] || { echo Cancelled; exit 1; }; \
	rm -f "$(REPO)/progress.json"; git -C "$(REPO)" add -A -- progress.json 2>/dev/null || true; \
	git -C "$(REPO)" commit -q -m "drill: reset progress" 2>/dev/null || true; \
	echo "Server progress cleared. Also click 'Reset all progress' in the app: the browser keeps its own copy."

ex-start:
	@$(PY) ex.py start $(EX) $(L) --repo "$(REPO)"

ex-check:
	@$(PY) ex.py check $(EX) $(L) --repo "$(REPO)" $(PUSHFLAG)

clean:
	@rm -f .server.pid .server.log; find . -name __pycache__ -prune -exec rm -rf {} \;
