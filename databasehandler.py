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
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute("truncate table " + table)
    connection.commit()
    connection.close()


def createtable(table, params):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    executestring = "create table if not exists " + table
    if len(params) > 0:
        executestring = executestring + " ("
        for param in params:
            executestring = executestring + param + ", "
        executestring = executestring[:-2] + ")"
    print("STRING:\n" + executestring)
    cursor.execute(executestring)
    connection.commit()
    connection.close()


def getplayers():
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute("select * from players")
    players = cursor.fetchall()
    connection.close()
    return players


def checksqliteversion():
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute("SELECT sqlite_version();")
    res = cursor.fetchall()
    connection.close()
    return res





