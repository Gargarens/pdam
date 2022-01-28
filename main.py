import requests
import json
import datetime
import hashlib

t = datetime.datetime.utcnow()
timestamp = "{}{:02d}{:02d}{:02d}{:02d}{:02d}".format(t.year, t.month, t.day, t.hour, t.minute, t.second)

api = "https://api.smitegame.com/smiteapi.svc/"
devid = "4187"
authkey = "EF4EA7FDE91144CAABABE5AE71129907"


def signature(method):
    return hashlib.md5((devid + method + authkey + timestamp).encode()).hexdigest()


createsessionstring = api + "createsessionJson/" + devid + "/" + signature("createsession") + "/" + timestamp
sessionid = requests.get(createsessionstring).json()["session_id"]


def call(params):
    callstring = api + params[0] + "Json/" + devid + "/" + signature(params[0]) + "/" + sessionid + "/" + timestamp
    for param in params:
        callstring = callstring + "/" + param
    return callstring


print(sessionid)
