from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.orm import declarative_base

Base = declarative_base()

enabled_players = ["creviceguy", "Spuik", "MeatEater04"]
enabled_players_id = ["1932674", "1922769", "716965538"]
modes = {
    "426":   "Conquest",
    "435":   "Arena",
    "448":   "Joust",
    "445":   "Assault",
    "10195": "Under 30 Arena",
    "451":   "Conquest Ranked",
    "10193": "Under 30 Conquest",
    "10197": "Under 30 Joust",
    "450":   "Joust Ranked",
    "10189": "Slash",
    "440":   "Duel Ranked"
}


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


tables = []
for player in enabled_players:
    for mode in modes.keys():
        tables.append(Table(
            player + "_" + mode,
            Base.metadata,
            Column("god", String, primary_key=True),
            Column("damage", Integer, default=0),
            Column("mitigated", Integer, default=0),
            Column("kills", Integer, default=0),
            Column("assists", Integer, default=0),
            Column("healing", Integer, default=0),
            Column("selfhealing", Integer, default=0)
        ))