VENV        := .venv
PY          := $(VENV)/bin/python
PIP         := $(VENV)/bin/pip

.PHONY: all install run-publisher run-subscriber clean distclean

all: install

$(VENV):
	python3 -m venv $(VENV)

install: $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run-publisher:
	$(PY) publisher.py

run-subscriber:
	$(PY) subscriber.py -d "CD Projekt" Ubisoft -t RPG

clean:
	rm -f $(GEN_PY)
	rm -rf __pycache__

distclean: clean
	rm -rf $(VENV)
