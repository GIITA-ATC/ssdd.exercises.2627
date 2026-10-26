PYTHON=python3
VENV=venv
ACTIVATE=. $(VENV)/bin/activate;

.PHONY: all install proto run-server run-client clean distclean

all: install proto

venv:
	$(PYTHON) -m venv $(VENV)

install: venv
	$(ACTIVATE) pip install --upgrade pip
	$(ACTIVATE) pip install -r requirements.txt

proto:
	$(ACTIVATE) python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. app.proto

run-server:
	$(ACTIVATE) python server.py

ARGS=-m
run-client:
	$(ACTIVATE) python client.py localhost:10001 $(ARGS)

clean:
	rm -f *_pb2.py *pb2_grpc.py
	rm -rf __pycache__

distclean: clean
	rm -rf $(VENV)
