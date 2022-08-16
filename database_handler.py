from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import db_models

# engine = create_engine('sqlite:///pdam.sqlite', echo=False)
engine = create_engine('postgres://eqqawghmzbrspv:8d24308bbef2127c5c9d9ae3fdae507569f788ad6a60c4a619dd055ef398de1a@ec2-54-75-26-218.eu-west-1.compute.amazonaws.com:5432/de176gevbt1ads', echo=False)
metadata = db_models.Base.metadata
metadata.create_all(engine)
Session = sessionmaker()
local_session = Session(bind=engine)
db = SQLAlchemy()


def get_gods_db():
    god_data = Session(bind=engine).query(db_models.Gods).order_by(db_models.Gods.name)
    return god_data


def get_players_db():
    return Session(bind=engine).query(db_models.Players)


def get_data(table):
    # return all columns
    return Session(bind=engine).query(table)


def insert(entry):
    local_session.add(entry)
    local_session.commit()


def insert_into(table, values):
    engine.execute(table.insert().values(values))
    local_session.commit()


def get_tables():
    return metadata.sorted_tables


def get_table(tablename):
    return metadata.tables[tablename]


def found_god(name):
    return get_gods_db().filter_by(name=name).first()


def found_player(pid):
    return get_players_db().filter_by(player_id=pid).first()


def found_god_in_table(table, name):
    return get_data(table).filter_by(god=name).first()


def execute(statement):
    engine.execute(statement)
