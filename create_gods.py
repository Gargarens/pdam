from app import Gods, Session, engine

local_session = Session(bind=engine)
new_god = Gods("Achilles", "Warrior", "Greek")
local_session.add(new_god)
local_session.commit()