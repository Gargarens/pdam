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
    players = getplayers()
    columns = ["god", "conquest", "arena", "joust", "assault", "under30arena", "conquestranked", "under30conquest",
                 "under30joust", "joustranked", "slash", "duelranked"]
    for player in players:
        name = player[1]
        createtable(name, columns)
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


@application.route("/player", methods=["POST", "GET"])
def player():
    global sessionid
    playername = "BigGirl2003"
    playerdata = getplayer(playername, sessionid)[0]
    playerid = playerdata["Id"]
    matchhistory = getmatchhistory(playerid, sessionid)
    arenamatches = []
    under30arenamatches = []
    for match in matchhistory:
        if match["Match_Queue_Id"] == 435:
            arenamatches.append(match)
        elif match["Match_Queue_Id"] == 10195:
            under30arenamatches.append(match)

    print("Found " + str(len(arenamatches)) + " arena matches and " + str(len(under30arenamatches)) + " under30arena matches for " + playername + ".")
    return render_template("player.html")


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
    playername = "Spuik"
    playerid = getplayerid(playername)
    recent = getmatchhistory(playerid, sessionid)
    print(recent[0])
    return render_template("update.html")
