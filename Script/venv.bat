cd ..\backend
mkdir .venv
python -m venv .venv
call .venv\Scripts\activate.bat
cd ..\Script
pip install -r requirements.txt
cd ..\backend 
python app.py