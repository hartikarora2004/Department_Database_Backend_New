# Setup Virtual Env (in root directory)
- pip install virtualenv
- python -m venv env
- source env/bin/activate

### Now install all libraries after activating the venv (make sure you setup venv before installing requirements as there might be a conflict with previously installed libraries)
- pip install -r requirements.txt

## Deactivate venv
- deactivate

## To run the project
- python3 manage.py makemigrations
- python3 manage.py migrate
- python3 manage.py runserver
