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
    return hashlib.md5((devid + method + authkey + timestamp).encode()).hexdigest().lower()


createsessionstring = api + "createsessionjson/" + devid + "/" + signature("createsession") + "/" + timestamp
# sessionid = requests.get(createsessionstring).json()["session_id"]
sessionid = "EE1DC8B7CC6B430BBEC5D7F8D195DC9B"
print("sessionid: " + sessionid)


def call(params):
    callstring = api + params[0] + "json/" + devid + "/" + signature(params[0]) + "/" + sessionid + "/" + timestamp
    for param in params[1:]:
        callstring = callstring + "/" + param
    return callstring


testresult = requests.get(call(["testsession"]))
# sample = "https://api.smitegame.com/smiteapi.svc/testsessionjson/1004/0abd990b4ca9f86817e087ad684515db" \
#          "/83B082E576584DA8B1DB073DECA9E819/20120927193800/HirezPlayer "
# print(sample)
# print("")
print(testresult.json())
