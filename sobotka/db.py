from peewee import * 
import os
from os.path import expanduser

def get_database():
	sobotka_app_data_path = expanduser('~/.sobotka')
	if not os.path.exists(sobotka_app_data_path):
	    os.makedirs(sobotka_app_data_path)

	db = SqliteDatabase(expanduser('~/.sobotka/sobotka.db'))
	return db

def create_tables(project):
    db = get_database()
    db.connect()
    try:
        db.create_tables([project])  
    except OperationalError:
        pass
