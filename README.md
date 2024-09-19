Setting Up the Project Locally

Clone the Repository:
https://github.com/Jawad652923/Travel_CRM.git
cd Travel_CRM 

Create and Activate a Virtual Environment:
python -m venv venv
venv\Scripts\activate

Install Dependencies:
pip install -r requirements.txt

Configure the Database
Update the DATABASES setting in settings.py . comment out the postgresql database settings and uncomment the default database settings

Run Migrations:
python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver

The API will be accessible at http://127.0.0.1:8000/.
