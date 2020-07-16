set app=tamer_app_document
python manage.py startapp %app%

cd %app%
mkdir templates

nul > commons.py
nul > forms.py
nul > tables.py
nul > urls.py
