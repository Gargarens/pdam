from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import db_models

engine = create_engine('sqlite:///testicle.sqlite', echo=True)
db_models.Base.metadata.create_all(engine)
Session = sessionmaker()
local_session = Session(bind=engine)
db = SQLAlchemy()


def get_gods_db():
    god_data = local_session.query(db_models.Gods).all()
    return god_data


def get_data(table):
    # return all columns
    return "Agni", 0, 0, 0, 0, 0, 0
