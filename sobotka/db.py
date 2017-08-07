from peewee import * 
from models import Project

def setup(Project):
    db = SqliteDatabase('sobotka.db')
    db.connect()
    try:
        db.create_tables([Project])  
    except OperationalError:
        pass
