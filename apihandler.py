import requests
import datetime
import hashlib

api = "https://api.smitegame.com/smiteapi.svc/"
devid = "4187"
authkey = "EF4EA7FDE91144CAABABE5AE71129907"


def signature(method):
    return hashlib.md5((devid + method + authkey + timestamp(datetimenow())).encode()).hexdigest().lower()


def timestamp(t):
    return "{}{:02d}{:02d}{:02d}{:02d}{:02d}".format(t.year, t.month, t.day, t.hour, t.minute, t.second)


def datetimenow():
    return datetime.datetime.utcnow()


def getSessionID():
    time = datetimenow()
    ts = timestamp(time)
    createsessionstring = api + "createsessionjson/" + devid + "/" + signature("createsession") + "/" + ts
    sessionid = requests.get(createsessionstring).json()["session_id"]
    #print("SESSION ID:\n" + sessionid)
    return sessionid, ts, time


def callString(params, sessionid):
    # params is list with method name (i.e. "createsession") as first element
    # and any possible parameters after {timestamp} as next elements
    callstring = api + params[0] + "json/" + devid + "/" + signature(params[0]) + "/" \
                 + sessionid + "/" + timestamp(datetimenow())
    for param in params[1:]:
        callstring = callstring + "/" + param
    print("CALLSTRING (" + params[0] + "):\n" + callstring)
    return callstring


def requestFromAPI(url):
    result = requests.get(url).json()
    return result


def testSession(sessionid):
    # testsessionstring = api + "testsessionjson" + "/" + devid + "/" + signature("testsession") + "/" + sessionid + "/" + timestamp(datetimenow())
    testsessionstring = callString(["testsession"], sessionid)
    return requestFromAPI(testsessionstring)


def checkdatause(sessionid):
    checkstring = callString(["getdataused"], sessionid)
    return requestFromAPI(checkstring)


def getplayer(player, sessionid):
    return requestFromAPI(callString(["getplayer", player], sessionid))


def getmatchhistory(playerid, sessionid):
    return requestFromAPI(callString(["getmatchhistory", str(playerid)], sessionid))


def getmatchidsbyqueue(queue, date, hour, sessionid):
    return requestFromAPI(callString(["getmatchidsbyqueue", str(queue), date, hour], sessionid))
    # Date format: 20171231
    # hour = 0...23 or by each 10min like so: "3,00" or "3,50"
    # QUEUE ID
    # 426   conquest
    # 435   arena
    # 448   joust
    # 445   assault
    # 466   clash
    # 10195 under 30 arena
    # 451   conquest ranked
    # 434   motd
    # 10193 under 30 conquest
    # 10197 under 30 joust
    # 459   siege
    # 450   joust ranked
    # 10189 slash
    # 440   duel ranked