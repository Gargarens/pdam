import datetime
from databasehandler import *
from apihandler import *
from flask import Flask, render_template, request, flash

application = Flask(__name__)
application.secret_key = "cockandballs"
time_since_start = 0
sessionid = 0
session_start_time = datetime.datetime.utcnow()


@application.route("/")
def index():
    # flash("Player name")
    return render_template("index.html")


@application.route("/createtables", methods=["POST", "GET"])
def createtables():
    # ALL COMMENTED OUT TO NOT FUCK UP THE DATABASE
    # players = getplayersdb()
    # tables = ["426", "435", "448", "445", "10195", "451", "10193", "10197", "450", "10189", "440"]
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
    #     for table in tables:
    #         tablename = name + "_" + table
    #         createtable(tablename, columns)
    #         sql = "INSERT INTO " + tablename + " values (?, ?, ?, ?, ?, ?, ?)"
    #         sqlexecutemany(sql, rows)
    flash("Add new gods manually")

    return render_template("createtables.html")


@application.route("/start", methods=["POST", "GET"])
def start():
    global sessionid
    global time_since_start
    global session_start_time
    sessionid, session_start_timestamp, session_start_time = getSessionID()
    # time_since_start = apihandler.datetimenow() - session_start_time
    # flash("Session ID: " + str(session_id))
    # flash("Session start time: " + str(session_start_time))
    # flash("Time since start: " + helper.timeDeltaToMinSec(str(time_since_start)))
    return render_template("start.html")


@application.route("/arena", methods=["POST", "GET"])
def arena():
    global sessionid
    playername = "creviceguy"
    date = "20220427"
    hour = "20"
    #arenadata = apihandler.getmatchidsbyqueue(435, date, hour, session_id)
    #print("Matches for " + date + ", hour " + hour + ":")
    #print(arenadata)
    return render_template("arena.html")


@application.route("/check", methods=["POST", "GET"])
def check():
    global time_since_start
    global sessionid
    global session_start_time
    time_since_start = datetimenow() - session_start_time
    datausedcheck = checkdatause(sessionid)[0]

    requestsLeft = datausedcheck['Request_Limit_Daily'] - datausedcheck['Total_Requests_Today']
    flash("Requests left: " + str(requestsLeft))

    activeSessions = datausedcheck['Active_Sessions']
    flash("Active sessions: " + str(activeSessions))

    sessionsLeft = datausedcheck['Session_Cap'] - datausedcheck['Total_Sessions_Today']
    flash("Sessions left: " + str(sessionsLeft))

    return render_template("check.html")


@application.route("/gods", methods=["POST", "GET"])
def gods():
    global sessionid
    god_data = getgods(sessionid)
    dbdata = []
    for god in god_data:
        dbdata.append((god["Name"], god["Roles"], god["Pantheon"]))
    insertintotable(dbdata, "gods")

    return render_template("gods.html")


@application.route("/update", methods=["POST", "GET"])
def update():
    global sessionid
    players = getplayersdb()
    for player in players:
        playerid = player[0]
        playername = player[1]
        recent = getmatchhistory(playerid, sessionid)

        for match in recent:
            # Sometimes API returns just "None"s. Skip those matches
            go = True
            god = ""
            try:
                god = match["God"].replace("_", " ")
            except:
                print("Error for player " + playername)
                go = False
            if not go:
                break
            mode = str(match["Match_Queue_Id"])
            damage = match["Damage"]
            mitigated = match["Damage_Mitigated"]
            kills = match["Kills"]
            assists = match["Assists"]
            healing = match["Healing"]
            selfhealing = match["Healing_Player_Self"]
            table = playername + "_" + mode
            sql = "SELECT * FROM " + table + " WHERE god = '" + god + "'"
            tabledata = fetchsql(sql)
            if len(tabledata) > 0:
                top = tabledata[0]
            else:
                print("NOTHING IN DB-------------\nGod: " + god)
                break
            # (0:GOD, 1:DMG, 2:MIT, 3:KILL, 4:ASSIST, 5:HEAL, 6:SELFHEAL)
            if damage > top[1]:
                sql = "UPDATE " + table + " SET damage = " + str(damage) + " WHERE god='" + god + "'"
                runsql(sql)
            if mitigated > top[2]:
                sql = "UPDATE " + table + " SET mitigated = " + str(mitigated) + " WHERE god='" + god + "'"
                runsql(sql)
            if kills > top[3]:
                sql = "UPDATE " + table + " SET kills = " + str(kills) + " WHERE god='" + god + "'"
                runsql(sql)
            if assists > top[4]:
                sql = "UPDATE " + table + " SET assists = " + str(assists) + " WHERE god='" + god + "'"
                runsql(sql)
            if healing > top[5]:
                sql = "UPDATE " + table + " SET healing = " + str(healing) + " WHERE god='" + god + "'"
                runsql(sql)
            if selfhealing > top[6]:
                sql = "UPDATE " + table + " SET selfhealing = " + str(selfhealing) + " WHERE god='" + god + "'"
                runsql(sql)
    return render_template("update.html")


@application.route("/scoreboard", methods=["POST", "GET"])
def scoreboard():
    return render_template("scoreboard.html")