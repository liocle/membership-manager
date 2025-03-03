#!/bin/sh
set -e  # Exit immediately if any command fails -> builtin, see: man bash


echo "🚀 Running database migrations..."
python create_tables.py  # Ensure tables exist

echo "✅ Starting FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
