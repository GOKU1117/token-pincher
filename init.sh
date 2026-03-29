#!/bin/bash

set -e

echo "🦀 TokenPincher starting..."

if [ ! -d "venv" ]; then
  echo "📦 Creating virtual environment..."
  python3 -m venv venv
fi

source venv/bin/activate

echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🚀 Starting backend..."
uvicorn api.server:app --reload &

sleep 2

echo "🌐 Opening frontend..."
if [[ "$OSTYPE" == "darwin"* ]]; then
  open frontend/index.html
else
  xdg-open frontend/index.html
fi

echo "✅ TokenPincher is running"