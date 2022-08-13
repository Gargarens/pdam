import sqlite3
# db = "pdam.sqlite"
# db = "postgres://eqqawghmzbrspv:8d24308bbef2127c5c9d9ae3fdae507569f788ad6a60c4a619dd055ef398de1a@ec2-54-75-26-218." \
#      "eu-west-1.compute.amazonaws.com:5432/de176gevbt1ads"
db = "testicle.sqlite"


def insertintotable(data, table, columns):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = "create table if not exists " + table + columns
    cursor.execute(sql)
    sql = "insert into " + table + " values (?,?,?)"
    cursor.executemany(sql, data)
    connection.commit()
    connection.close()


def truncatetable(table):
    sql = "truncate table " + table
    runsql([sql])


def createtable(table, params):
    sql = "create table if not exists " + table
    if len(params) > 0:
        sql = sql + " ("
        for param in params:
            sql = sql + param + ", "
        sql = sql[:-2] + ")"
    runsql([sql])


def getplayersdb():
    createtable("players", ["player_id TEXT PRIMARY KEY", "name TEXT"])
    sql = "select * from players"
    return fetchsql(sql)


def checksqliteversion():
    sql = "SELECT sqlite_version();"
    return fetchsql(sql)


def getplayerid(playername):
    sql = "SELECT player_id FROM players WHERE name='" + playername + "'"
    playerid = str(fetchsql(sql)[0][0])
    return playerid


def runsql(sqlarray):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    for sql in sqlarray:
        cursor.execute(sql)
    connection.commit()
    connection.close()


def sqlexecutemany(sql, values):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    print("SQL:\n" + sql + "\nVALUES:")
    print(values)
    cursor.executemany(sql, values)
    connection.commit()
    connection.close()


def fetchsql(sql):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    connection.close()
    return result


def getgodsdb():
    sql = "select name, role from gods"
    return fetchsql(sql)


def getgodnamesdb():
    sql = "create table if not exists gods (name TEXT, role TEXT, pantheon TEXT)"
    runsql([sql])
    sql = "select name from gods"
    return fetchsql(sql)


def gettop(table, column):
    sql = "SELECT MAX(" + column + ") FROM " + table
    maxvalue = fetchsql(sql)[0][0]
    sql = "SELECT god, " + column + " FROM " + table + " WHERE " + column + "=" + str(maxvalue)
    result = fetchsql(sql)[0]
    return result


def gettopforgod(table, column, god):
    sql = "SELECT " + column + " FROM " + table + " WHERE god = '" + god + "'"
    result = fetchsql(sql)[0][0]
    return result


def getdata(table):
    # sql = "SELECT damage, mitigated, kills, assists, healing, selfhealing FROM " + table
    sql = "SELECT * FROM " + table
    result = fetchsql(sql)
    return result
