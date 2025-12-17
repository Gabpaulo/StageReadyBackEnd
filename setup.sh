#!/bin/bash

# Setup script for Stage Ready Backend

echo "Creating virtual environment..."
python -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate || source venv/Scripts/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Creating Django project..."
django-admin startproject stage_ready_api .

echo "Creating speech_coach app..."
python manage.py startapp speech_coach

echo "Setup complete!"
echo "To activate the virtual environment:"
echo "  On Linux/Mac: source venv/bin/activate"
echo "  On Windows: venv\\Scripts\\activate"
