#!/bin/bash
set -e

echo "Setting up Sentinel AI India..."

python -m venv venv
source venv/Scripts/activate

pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

pre-commit install

echo "Running tests..."
pytest tests/ -v

echo "Setup complete. Run 'streamlit run app.py' to start the dashboard."