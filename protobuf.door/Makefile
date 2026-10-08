VENV        := .venv
PY          := $(VENV)/bin/python
PIP         := $(VENV)/bin/pip
PROTO_NAME  := door
GEN_PY      := $(PROTO_NAME)_pb2.py

HOST        := localhost
PORT        := 10001

.PHONY: all install run-server open_door close_door get_door_status clean distclean

all: install $(GEN_PY)

$(VENV):
	python3 -m venv $(VENV)

install: $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

$(GEN_PY): $(PROTO_NAME).proto
	$(PY) -m grpc_tools.protoc -I=. --python_out=. $(PROTO_NAME).proto

run-server:
	$(PY) door.py $(PORT)

open_door:
	$(PY) controller.py $(HOST) $(PORT) open -t 30 -m pedestrian

close_door:
	$(PY) controller.py $(HOST) $(PORT) close

get_door_status:
	$(PY) controller.py $(HOST) $(PORT) status

clean:
	rm -f $(GEN_PY)
	rm -rf __pycache__

distclean: clean
	rm -rf $(VENV)
