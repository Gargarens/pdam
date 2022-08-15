from apihandler import getSessionID, getmatchhistory
from database_handler import get_players_db, get_table, get_data, execute


def updateDB(enabled_players, modes):
    session_id, session_start_timestamp, session_start_time = getSessionID()
    players = get_players_db()
    for player in players:
        player_id = player.player_id
        player_name = player.name
        if player_name not in enabled_players:
            print("Skipping " + player_name + " because it's not in the list of "
                                              "enabled players.")
            continue
        print("Updating " + player_name)
        recent = getmatchhistory(player_id, session_id)

        for match in recent:
            # Sometimes API returns just "None"s. Skip those matches
            go = True
            god = ""
            try:
                god = match["God"].replace("_", " ")
            except:
                print("Error for player " + player_name)
                go = False
            if god == "ChangE":
                god = "Chang'e"
            if not go:
                continue
            mode = str(match["Match_Queue_Id"])
            if mode not in modes.keys():
                continue
            damage = match["Damage"]
            mitigated = match["Damage_Mitigated"]
            kills = match["Kills"]
            assists = match["Assists"]
            healing = match["Healing"]
            selfhealing = match["Healing_Player_Self"]
            tablename = player_name + "_" + mode
            table = get_table(tablename)
            top = get_data(table).filter_by(god=god).all()
            if len(top) > 0:
                top = top[0]
            else:
                print("NOTHING IN DB-------------\nGod: " + god)
                continue

            # (0:GOD, 1:DMG, 2:MIT, 3:KILL, 4:ASSIST, 5:HEAL, 6:SELF HEAL)
            if damage > top[1]:
                execute(table.update().where(table.c.god == god).values(damage=damage))
            if mitigated > top[2]:
                execute(table.update().where(table.c.god == god).values(mitigated=mitigated))
            if kills > top[3]:
                execute(table.update().where(table.c.god == god).values(kills=kills))
            if assists > top[4]:
                execute(table.update().where(table.c.god == god).values(assists=assists))
            if healing > top[5]:
                execute(table.update().where(table.c.god == god).values(healing=healing))
            if selfhealing > top[6]:
                execute(table.update().where(table.c.god == god).values(selfhealing=selfhealing))