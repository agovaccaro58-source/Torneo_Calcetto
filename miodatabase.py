import mysql.connector

def connetti():
    return mysql.connector.connect(
        host="localhost",
        user="studente",
        password="studente",
        database="calcetto"
    )