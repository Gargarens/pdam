from databasehandler import *
from apihandler import *
from flask import Flask, render_template, flash
from flask_apscheduler import APScheduler
from updateDB import updateDB
from flask_sqlalchemy import SQLAlchemy
import datab

app = Flask(__name__)
app.secret_key = "cockandballs"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testicle.sqlite'
scheduler = APScheduler()
db = SQLAlchemy(app)
time_since_start = 0
session_id = 0
session_start_time = datetime.datetime.utcnow()
# mode_keys = ["426", "435", "448", "445", "10195", "451", "10193", "10197", "450", "10189", "440"]
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


def updateTask():
    updateDB(enabled_players, modes.keys())


scheduler.add_job(id="update-db", func=updateTask, trigger="interval", seconds=600)
scheduler.start()


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/createtables", methods=["POST", "GET"])
def createtables():
    # ALL COMMENTED OUT TO NOT FUCK UP THE DATABASE
    # players = getplayersdb()
    #
    # # Just hardcode insert players into db
    # if len(players) == 0:
    #     sqlexecutemany("INSERT INTO players values (?, ?)",
    #                    [(1922769, "Spuik"), (1932674, "creviceguy"), (716965538, "MeatEater04")])
    #
    # columns = ["god TEXT PRIMARY KEY", "damage INTEGER DEFAULT (0)", "mitigated INTEGER DEFAULT (0)",
    #            "kills INTEGER DEFAULT (0)", "assists INTEGER DEFAULT (0)", "healing INTEGER DEFAULT (0)",
    #            "selfhealing INTEGER DEFAULT (0)"]
    # godsfromdb = getgodsdb()
    # gods = []
    # rows = []
    # for tuple in godsfromdb:
    #     gods.append(tuple[0])
    # for god in gods:
    #     values = (god, 0, 0, 0, 0, 0, 0)
    #     rows.append(values)
    # for player in players:
    #     name = player[1]
    #     for table in modes:
    #         tablename = name + "_" + table
    #         createtable(tablename, columns)
    #         sql = "INSERT INTO " + tablename + " values (?, ?, ?, ?, ?, ?, ?)"
    #         sqlexecutemany(sql, rows)

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


class Gods(db.Model):
    name = db.Column(db.String, primary_key=True)
    role = db.Column(db.String, nullable=False)
    pantheon = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<God %r>' % self.name

    def __init__(self, name, role, pantheon):
        self.name = name
        self.role = role
        self.pantheon = pantheon


class Players(db.Model):
    player_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return '<Player %r>' % self.name

    def __init__(self, pid, name):
        self.player_id = pid
        self.name = name


@app.route("/gods", methods=["POST", "GET"])
def gods():
    global session_id
    global session_start_time
    db.create_all()
    god_data = datab.data  # god_data = getgods(session_id)

    for entry in god_data:
        found_god = Gods.query.filter_by(name=entry["Name"]).first()
        if found_god:
            print(found_god, end=" ")
            print("already in database")
        else:
            god = Gods(entry["Name"], entry["Roles"], entry["Pantheon"])
            db.session.add(god)

    for pid, name in zip(enabled_players_id, enabled_players):
        found_player = Players.query.filter_by(player_id=pid).first()
        if found_player:
            print(found_player, end=" ")
            print("already in database")
        else:
            player = Players(pid, name)
            db.session.add(player)

    db.session.commit()
    return render_template("gods.html")


@app.route("/update", methods=["POST", "GET"])
def update():
    session_id, session_start_timestamp, session_start_time = getSessionID()
    # updateDB(enabled_players, mode_keys)
    players = Players.query.all()
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
        if god == "ChangE":
            god = "Chang''e"
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
        table = player_name + "_" + mode
        sql = "SELECT * FROM " + table + " WHERE god = '" + god + "'"
        tabledata = fetchsql(sql)
        print(tabledata)
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
    for godtuple in getgodsdb():
        god = godtuple[0]
        role = godtuple[1]
        if role == "Mage, Ranged": # Fix bug in API with Persephone role
            role = "Mage"
        gods.append(god)
        roles[god] = role
    for mode in modes:
        data[mode] = {}
        for player in enabled_players:
            table = player + "_" + mode
            res = getdata(table)
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
                    entry.append(data[mode][player][j][i+1])
                rows[columns[i]].append(entry)
        tables[mode] = rows
    return render_template("scores.html", tableheaders=enabled_players, gods=gods, roles=roles, tables=tables, len=len)


if __name__ == "__main__":
    app.run(port=1234, debug=True, use_reloader=False)


class creviceguy_426(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class creviceguy_435(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class creviceguy_448(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class creviceguy_445(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class creviceguy_10195(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class creviceguy_451(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class creviceguy_10193(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class creviceguy_10197(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class creviceguy_450(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class creviceguy_10189(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class creviceguy_440(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class Spuik_426(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class Spuik_435(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class Spuik_448(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class Spuik_445(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class Spuik_10195(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class Spuik_451(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class Spuik_10193(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class Spuik_10197(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class Spuik_450(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class Spuik_10189(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class Spuik_440(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class Meateater04_426(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class Meateater04_435(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class Meateater04_448(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class Meateater04_445(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class Meateater04_10195(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class Meateater04_451(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class Meateater04_10193(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class Meateater04_10197(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class Meateater04_450(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class Meateater04_10189(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)


class Meateater04_440(db.Model):
    god = db.Column(db.String, primary_key=True)
    damage = db.Column(db.Integer, default=0)
    mitigated = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    healing = db.Column(db.Integer, default=0)
    selfhealing = db.Column(db.Integer, default=0)
