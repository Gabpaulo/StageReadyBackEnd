@echo off

REM Setup script for Stage Ready Backend (Windows)

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Creating Django project...
django-admin startproject stage_ready_api .

echo Creating speech_coach app...
python manage.py startapp speech_coach

echo.
echo Setup complete!
echo To activate the virtual environment: venv\Scripts\activate
