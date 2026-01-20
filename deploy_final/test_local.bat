@echo off
echo Testing deployment package locally...
python -m venv venv_test
call venv_test\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python app.py
