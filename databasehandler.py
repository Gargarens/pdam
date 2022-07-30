import sqlite3
db = "pdam.sqlite"


def insertintotable(data, table):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    executestring = "insert into " + table + " values (?,?,?)"
    print(executestring)
    print("************************")
    cursor.executemany(executestring, data)
    connection.commit()
    connection.close()


def truncatetable(table):
    sql = "truncate table " + table
    runsql(sql)


def createtable(table, params):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    executestring = "create table if not exists " + table
    if len(params) > 0:
        executestring = executestring + " ("
        for param in params:
            executestring = executestring + param + ", "
        executestring = executestring[:-2] + ")"
    cursor.execute(executestring)
    connection.commit()
    connection.close()


def getplayers():
    sql = "select * from players"
    return fetchsql(sql)


def checksqliteversion():
    sql = "SELECT sqlite_version();"
    return fetchsql(sql)


def getplayerid(playername):
    sql = "SELECT player_id FROM players WHERE name='" + playername + "'"
    playerid = str(fetchsql(sql)[0][0])
    return playerid


def runsql(sql):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()


def sqlexecutemany(sql, values):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    #print("SQL:\n" + sql + "\nVALUES:")
    #print(values)
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
    sql = "select name from gods"
    return fetchsql(sql)
