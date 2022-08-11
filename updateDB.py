from databasehandler import runsql, getplayersdb, fetchsql
from apihandler import getSessionID, getmatchhistory


def updateDB(enabled_players, mode_keys):
    session_id, session_start_timestamp, session_start_time = getSessionID()
    players = getplayersdb()
    verbose = False
    for player in players:
        player_id = player[0]
        player_name = player[1]
        if player_name not in enabled_players:
            print("Skipping " + player_name + " because it's not in the list of "
                  "enabled players.")
            continue
        # print("Updating " + player_name)
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
                god = "Chang''e"
            # print("God: " + god)
            if not go:
                continue
            mode = str(match["Match_Queue_Id"])
            if mode not in mode_keys:
                continue
            damage = match["Damage"]
            mitigated = match["Damage_Mitigated"]
            kills = match["Kills"]
            assists = match["Assists"]
            healing = match["Healing"]
            selfhealing = match["Healing_Player_Self"]
            table = player_name + "_" + mode
            sql = "SELECT * FROM " + table + " WHERE god = '" + god + "'"
            tabledata = fetchsql(sql)
            if len(tabledata) > 0:
                top = tabledata[0]
            else:
                print("NOTHING IN DB-------------\nGod: " + god)
                continue
            # (0:GOD, 1:DMG, 2:MIT, 3:KILL, 4:ASSIST, 5:HEAL, 6:SELF HEAL)
            if damage > top[1]:
                sql = "UPDATE " + table + " SET damage = " + str(damage) + " WHERE god='" + god + "'"
                if verbose:
                    print("New damage PR for " + player_name + "(" + god + ")")
                runsql(sql)
            if mitigated > top[2]:
                sql = "UPDATE " + table + " SET mitigated = " + str(mitigated) + " WHERE god='" + god + "'"
                if verbose:
                    print("New mitigated PR for " + player_name + "(" + god + ")")
                runsql(sql)
            if kills > top[3]:
                sql = "UPDATE " + table + " SET kills = " + str(kills) + " WHERE god='" + god + "'"
                if verbose:
                    print("New kills PR for " + player_name + "(" + god + ")")
                runsql(sql)
            if assists > top[4]:
                sql = "UPDATE " + table + " SET assists = " + str(assists) + " WHERE god='" + god + "'"
                if verbose:
                    print("New assists PR for " + player_name + "(" + god + ")")
                runsql(sql)
            if healing > top[5]:
                sql = "UPDATE " + table + " SET healing = " + str(healing) + " WHERE god='" + god + "'"
                if verbose:
                    print("New healing PR for " + player_name + "(" + god + ")")
                runsql(sql)
            if selfhealing > top[6]:
                sql = "UPDATE " + table + " SET selfhealing = " + str(selfhealing) + " WHERE god='" + god + "'"
                if verbose:
                    print("New selfhealing PR for " + player_name + "(" + god + ")")
                runsql(sql)
