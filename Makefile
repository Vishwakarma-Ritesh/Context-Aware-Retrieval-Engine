PYTHON ?= python3

.PHONY: benchmark test api ingest rebuild

benchmark:
	$(PYTHON) -m app.main

test:
	$(PYTHON) -m pytest

api:
	$(PYTHON) -m uvicorn app.main:create_app --factory --host 0.0.0.0 --port 8000

ingest:
	$(PYTHON) scripts/ingest_documents.py

rebuild:
	$(PYTHON) scripts/rebuild_index.py
