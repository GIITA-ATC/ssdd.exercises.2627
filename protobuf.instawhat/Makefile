VENV        := .venv
PY          := $(VENV)/bin/python
PIP         := $(VENV)/bin/pip
PROTO_NAME  := instawhat
GEN_PY      := $(PROTO_NAME)_pb2.py

HOST        := localhost
PORT        := 10001

.PHONY: all install run-server post_photo comment_photo rate_photo like_photo delete_photo get_last_photos clean distclean

all: install $(GEN_PY)

$(VENV):
	python3 -m venv $(VENV)

install: $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

$(GEN_PY): $(PROTO_NAME).proto
	$(PY) -m grpc_tools.protoc -I=. --python_out=. $(PROTO_NAME).proto

run-server:
	$(PY) server.py $(PORT)

post_photo:
	$(PY) client.py $(HOST) $(PORT) post_photo "http://example.com/photo.jpg"

comment_photo:
	$(PY) client.py $(HOST) $(PORT) comment_photo Jane.Doe "http://example.com/photo.jpg" "Great photo!"

rate_photo:
	$(PY) client.py $(HOST) $(PORT) rate_photo Jane.Doe "http://example.com/photo.jpg" 5

like_photo:
	$(PY) client.py $(HOST) $(PORT) like_photo Jane.Doe "http://example.com/photo.jpg"

delete_photo:
	$(PY) client.py $(HOST) $(PORT) delete_photo "http://example.com/photo.jpg"

get_last_photos:
	$(PY) client.py $(HOST) $(PORT) get_last_photos Jane.Doe

clean:
	rm -f $(GEN_PY)
	rm -rf __pycache__

distclean: clean
	rm -rf $(VENV)
