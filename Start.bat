@echo Remember to configure config.json before starting!
@echo This may time us some time...

python -m venv venv
call venv\Scripts\activate.bat

pip install -r requirements.txt

python ./__init__.py