echo Creating VENV
python -m venv VENV
VENV\Scripts\activate.ps1
pip install -r requirement.txt
python main.py
pause