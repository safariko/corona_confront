# for Windows

cd corona_confront_master

python3 -m pip install --user virtualenv

python3 -m venv env

.\env\Scripts\activate

pip install -r requirements.txt

python3 manage.py collectstatic 

python3 manage.py migrate 

python3 manage.py runserver


# for MacOS

cd corona_confront_master

sudo -H pip install virtualenv

virtualenv venv

source venv/bin/activate

pip install -r requirements.txt

python3 manage.py collectstatic 

python3 manage.py migrate 

python3 manage.py runserver
