VENV        := .venv
PY          := $(VENV)/bin/python
PIP         := $(VENV)/bin/pip
ARGS        ?= request 2026-12-01T21:00 4 Ana 600123456

.PHONY: all install run-server run-client clean distclean

all: install

$(VENV):
	python3 -m venv $(VENV)

install: $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run-server:
	$(PY) server.py

run-client:
	$(PY) client.py $(ARGS)

clean:
	rm -rf __pycache__

distclean: clean
	rm -rf $(VENV)
