from databasehandler import *
from apihandler import *
from flask import Flask, render_template, flash
from flask_apscheduler import APScheduler
from updateDB import updateDB

app = Flask(__name__)
app.secret_key = "cockandballs"
scheduler = APScheduler()
time_since_start = 0
session_id = 0
session_start_time = datetime.datetime.utcnow()
mode_keys = ["426", "435", "448", "445", "10195", "451", "10193", "10197", "450", "10189", "440"]
enabled_players = ["creviceguy", "Spuik", "MeatEater04"]
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
    updateDB(enabled_players, mode_keys)


scheduler.add_job(id="update-db", func=updateTask, trigger="interval", seconds=600)
scheduler.start()


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/createtables", methods=["POST", "GET"])
def createtables():
    # ALL COMMENTED OUT TO NOT FUCK UP THE DATABASE
    players = getplayersdb()

    # Just hardcode insert players into db
    if len(players) == 0:
        sqlexecutemany("INSERT INTO players values (?, ?)",
                       [(1922769, "Spuik"), (1932674, "creviceguy"), (716965538, "MeatEater04")])

    columns = ["god TEXT PRIMARY KEY", "damage INTEGER DEFAULT (0)", "mitigated INTEGER DEFAULT (0)",
               "kills INTEGER DEFAULT (0)", "assists INTEGER DEFAULT (0)", "healing INTEGER DEFAULT (0)",
               "selfhealing INTEGER DEFAULT (0)"]
    godsfromdb = getgodsdb()
    gods = []
    rows = []
    for tuple in godsfromdb:
        gods.append(tuple[0])
    for god in gods:
        values = (god, 0, 0, 0, 0, 0, 0)
        rows.append(values)
    for player in players:
        name = player[1]
        for table in modes:
            tablename = name + "_" + table
            createtable(tablename, columns)
            sql = "INSERT INTO " + tablename + " values (?, ?, ?, ?, ?, ?, ?)"
            sqlexecutemany(sql, rows)

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

    requestsLeft = datausedcheck['Request_Limit_Daily'] - datausedcheck['Total_Requests_Today']
    flash("Requests left: " + str(requestsLeft))

    activeSessions = datausedcheck['Active_Sessions']
    flash("Active sessions: " + str(activeSessions))

    sessionsLeft = datausedcheck['Session_Cap'] - datausedcheck['Total_Sessions_Today']
    flash("Sessions left: " + str(sessionsLeft))

    return render_template("check.html")


@app.route("/gods", methods=["POST", "GET"])
def gods():
    global session_id
    global session_start_time
    god_data = getgods(session_id)
    existinggods = getgodnamesdb()
    existinggodnames = []
    for tuple in existinggods:
        existinggodnames.append(tuple[0])
    dbdata = []
    for god in god_data:
        if god["Name"] not in existinggodnames:
            dbdata.append((god["Name"], god["Roles"], god["Pantheon"]))
    insertintotable(dbdata, "gods", " (name TEXT, role TEXT, pantheon TEXT)")

    return render_template("gods.html")


@app.route("/update", methods=["POST", "GET"])
def update():
    updateDB(enabled_players, mode_keys)
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
    app.run()
