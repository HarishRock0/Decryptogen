#!/usr/bin/env sh
set -eu

uvicorn app:app --host 0.0.0.0 --port 8000 &
exec streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 7860 --server.headless true
