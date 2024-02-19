#!/bin/bash
cd /home/BACKEND_MLS-tutor/

# activate virtual environment
python3 -m venv devbackend_env
source devbackend_env/bin/activate

pip install psycopg2-binary gunicorn
pip install -r requirements.txt

python3 core/manage.py makemigrations
python3 core/manage.py migrate
