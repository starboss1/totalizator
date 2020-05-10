# Totalizator

3rd year course work, NaUKMA, Faculty of Computer Sciences, Software Engineering, created by **Sergei Konoshenko**

Cite: https://totalizator-course-work.herokuapp.com/

### Setup project
* Install Python 3 and PostgreSQL.
* Install requirements `pip install -r requirements.txt`
* Create file `.env` in the root and configure DB and Secret Key. Example:
```
DB_HOST = 'localhost'
DB_USER = 'postgres'
DB_NAME = 'some_db'
DB_PASS = 'mypass'
DB_PORT = '5432'
SECRET_KEY = 'my-secret-key'
```
* Write in console `python run.py` to run aplication
* Open browser http://localhost:8000/
