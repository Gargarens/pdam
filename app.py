from apihandler import *
from flask import Flask, render_template, flash
from flask_apscheduler import APScheduler
from db_models import Gods, Players, modes, enabled_players, enabled_players_id
from config import Config
import god_data_copy
from updateDB import updateDB
import database_handler


def register_extensions(application):
    from database_handler import db
    db.init_app(application)


def create_app():
    application = Flask(__name__)
    application.config.from_object(Config)
    register_extensions(application)
    return application


app = create_app()
app.secret_key = "cockandballs"
scheduler = APScheduler()
time_since_start = 0
session_id = 0
session_start_time = datetime.datetime.utcnow()


def updateTask():
    # updateDB(enabled_players, modes.keys())
    print("updated")


scheduler.add_job(id="update-db", func=updateTask, trigger="interval", seconds=600)
scheduler.start()


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/createtables", methods=["POST", "GET"])
def createtables():
    god_data = god_data_copy.data
    # god_data = getgods(session_id) # commented out to not blast API every time testing

    for entry in god_data:
        found_god = database_handler.found_god(entry["Name"])
        if found_god:
            # print(found_god, end=" ")
            # print("already in database")
            continue
        else:
            god = Gods(entry["Name"], entry["Roles"], entry["Pantheon"])
            # print("Inserting god: " + entry["Name"])
            database_handler.insert(god)

    for pid, name in zip(enabled_players_id, enabled_players):
        found_player = database_handler.found_player(pid)
        if found_player:
            # print(found_player, end=" ")
            # print("already in database")
            continue
        else:
            player = Players(pid, name)
            database_handler.insert(player)
            # print("Inserting player: " + player.name)

    for table in database_handler.get_tables():
        if table.name == "Gods" or table.name == "Players":
            continue
        else:
            # Build a list of rows and insert all at once, instead of inserting one by one. For SQL performance
            values = []
            for god in database_handler.get_gods_db():
                found_god = database_handler.found_god_in_table(table, god.name)
                if found_god:
                    # print("Already in database " + table.name + " - " + god.name)
                    continue
                else:
                    values.append({"god": god.name})
                    # print("Initiating " + god.name + " into " + table.name)
            if len(values) > 0:
                database_handler.insert_into(table, values)
    return render_template("createtables.html")


@app.route("/start", methods=["POST", "GET"])
def start():
    global session_id
    global time_since_start
    global session_start_time
    session_id, session_start_timestamp, session_start_time = getSessionID()
    return render_template("start.html")


@app.route("/check", methods=["POST", "GET"])
def check():
    global time_since_start
    global session_id
    global session_start_time
    time_since_start = datetimenow() - session_start_time
    datausedcheck = checkdatause(session_id)[0]

    requests_left = datausedcheck['Request_Limit_Daily'] - datausedcheck['Total_Requests_Today']
    flash("Requests left: " + str(requests_left))

    active_sessions = datausedcheck['Active_Sessions']
    flash("Active sessions: " + str(active_sessions))

    sessions_left = datausedcheck['Session_Cap'] - datausedcheck['Total_Sessions_Today']
    flash("Sessions left: " + str(sessions_left))

    return render_template("check.html")


@app.route("/update", methods=["POST", "GET"])
def update():
    session_id, session_start_timestamp, session_start_time = getSessionID()
    # updateDB(enabled_players, mode_keys)
    players = database_handler.get_players_db()
    print(players[0].player_id)
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
        # if god == "ChangE":
        #     god = "Chang''e"
        # print("God: " + god)
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
        table = database_handler.get_table(tablename)
        tabledata = database_handler.get_data(table).filter_by(god=god).all()
        print(god)
        print(tabledata)
        break
        # if len(tabledata) > 0:
        #     top = tabledata[0]
        #     print(top)
        # else:
        #     print("NOTHING IN DB-------------\nGod: " + god)
        #     continue
        # # (0:GOD, 1:DMG, 2:MIT, 3:KILL, 4:ASSIST, 5:HEAL, 6:SELF HEAL)
        # if damage > top[1]:
        #     sql = "UPDATE " + table + " SET damage = " + str(damage) + " WHERE god='" + god + "'"
        #     if verbose:
        #         print("New damage PR for " + player_name + "(" + god + ")")
        #     runsql([sql])
        # if mitigated > top[2]:
        #     sql = "UPDATE " + table + " SET mitigated = " + str(mitigated) + " WHERE god='" + god + "'"
        #     if verbose:
        #         print("New mitigated PR for " + player_name + "(" + god + ")")
        #     runsql([sql])
        # if kills > top[3]:
        #     sql = "UPDATE " + table + " SET kills = " + str(kills) + " WHERE god='" + god + "'"
        #     if verbose:
        #         print("New kills PR for " + player_name + "(" + god + ")")
        #     runsql([sql])
        # if assists > top[4]:
        #     sql = "UPDATE " + table + " SET assists = " + str(assists) + " WHERE god='" + god + "'"
        #     if verbose:
        #         print("New assists PR for " + player_name + "(" + god + ")")
        #     runsql([sql])
        # if healing > top[5]:
        #     sql = "UPDATE " + table + " SET healing = " + str(healing) + " WHERE god='" + god + "'"
        #     if verbose:
        #         print("New healing PR for " + player_name + "(" + god + ")")
        #     runsql([sql])
        # if selfhealing > top[6]:
        #     sql = "UPDATE " + table + " SET selfhealing = " + str(selfhealing) + " WHERE god='" + god + "'"
        #     if verbose:
        #         print("New selfhealing PR for " + player_name + "(" + god + ")")
        #     runsql([sql])
    return render_template("update.html")


@app.route("/", methods=["POST", "GET"])
def scores():
    columns = ["damage", "mitigated", "kills", "assists", "healing", "selfhealing"]
    data = {}
    tables = {}
    gods = []
    roles = {}
    for godtuple in database_handler.get_gods_db():
        god = godtuple[0]
        role = godtuple[1]
        if role == "Mage, Ranged":  # Fix bug in API with Persephone role
            role = "Mage"
        gods.append(god)
        roles[god] = role
    for mode in modes:
        data[mode] = {}
        for player in enabled_players:
            table = player + "_" + mode
            res = database_handler.get_data(table)
            data[mode][player] = res

    for mode in modes:
        damage, mitigated, kills, assists, healing, selfhealing = [], [], [], [], [], []
        rows = {
            "damage": damage,
            "mitigated": mitigated,
            "kills": kills,
            "assists": assists,
            "healing": healing,
            "selfhealing": selfhealing,
        }
        for j in range(len(gods)):
            for i in range(len(columns)):
                entry = []
                for player in enabled_players:
                    entry.append(data[mode][player][j][i + 1])
                rows[columns[i]].append(entry)
        tables[mode] = rows
    return render_template("scores.html", tableheaders=enabled_players, gods=gods, roles=roles, tables=tables, len=len)


if __name__ == "__main__":
    app.run(port=1234, debug=True, use_reloader=False)

