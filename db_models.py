from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Gods(Base):
    __tablename__ = "Gods"
    name = Column(String(), primary_key=True)
    role = Column(String(), nullable=False)
    pantheon = Column(String(), nullable=False)

    def __repr__(self):
        return '<God> %r' % self.name

    def __init__(self, name, role, pantheon):
        self.name = name
        self.role = role
        self.pantheon = pantheon


class Players(Base):
    __tablename__ = "Players"
    player_id = Column(String, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return '<Player> %r' % self.name

    def __init__(self, pid, name):
        self.player_id = pid
        self.name = name
