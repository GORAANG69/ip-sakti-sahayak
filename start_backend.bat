@echo off
cd /d "%~dp0backend"
if not exist ".venv\Scripts\python.exe" python -m venv .venv
call .venv\Scripts\activate.bat
pip install -r requirements.txt
if not exist ".env" copy ".env.example" ".env"
python run.py
pause
