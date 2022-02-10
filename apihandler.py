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
    return requests.get(createsessionstring).json()["session_id"], ts, time


def callString(params, sessionid):
    callstring = api + params[0] + "json/" + devid + "/" + signature(params[0]) + "/" \
                 + sessionid + "/" + timestamp(datetimenow()) + "/" + params[1]
    for param in params[1:]:
        callstring = callstring + "/" + param
    return callstring


def requestFromAPI(url):
    result = requests.get(url).json()
    return result


# testresult = requests.get(call(["testsession"]))
# sample = "https://api.smitegame.com/smiteapi.svc/testsessionjson/1004/0abd990b4ca9f86817e087ad684515db" \
#          "/83B082E576584DA8B1DB073DECA9E819/20120927193800/HirezPlayer "
# print(sample)
# print("")
# print(testresult.json())
