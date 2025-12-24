#!/bin/bash
# Start the FastAPI app in the background
uvicorn app:app --host 0.0.0.0 --port 8002 &
# Start the worker process
python worker.py
