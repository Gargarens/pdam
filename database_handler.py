from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
import db_models

# engine = create_engine('sqlite:///pdam.sqlite', echo=False)
# engine = create_engine('postgresql://postgres:p@localhost/masticle', echo=False)
engine = create_engine('postgresql://eqqawghmzbrspv:8d24308bbef2127c5c9d9ae3fdae507569f788ad6a60c4a619dd055ef398de1a@ec2-54-75-26-218.eu-west-1.compute.amazonaws.com:5432/de176gevbt1ads', echo=False)
metadata = db_models.Base.metadata
metadata.create_all(engine)
Session = sessionmaker()
local_session = Session(bind=engine)
db = SQLAlchemy()


def get_gods_db():
    session = Session(bind=engine)
    god_data = session.query(db_models.Gods).order_by(db_models.Gods.name)
    session.close()
    return god_data


def get_god_names_db():
    statement = select(metadata.tables["Gods"].c.name)
    return fetch(statement)


def get_players_db():
    statement = select(metadata.tables["Players"])
    result = fetch(statement)
    print(result)
    return result


def get_player_names_db():
    statement = select(metadata.tables["Players"].c.name)
    return fetch(statement)


def get_data_many(tablenames):
    session = Session(bind=engine)
    result = {}
    for tablename in tablenames:
        result[tablename] = session.query(metadata.tables[tablename]).order_by("god").all()
    session.close()
    return result


def insert(entry):
    local_session.add(entry)
    local_session.commit()
    local_session.close()


def insert_into(table, values):
    engine.execute(table.insert().values(values))
    local_session.commit()


def get_tables():
    return metadata.sorted_tables


def get_table(tablename):
    return metadata.tables[tablename]


def gods_in_table(table):
    statement = select(table.c.god)
    return fetch(statement)


def fetch(statement):
    connection = engine.connect()
    result = engine.execute(statement)
    connection.close()
    return result.all()


def execute(statement):
    connection = engine.connect()
    engine.execute(statement)
    connection.close()
