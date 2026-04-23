import mysql.connector


def get_connection():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="VTU26769@pavani",   
        database="university_db"
    )

    return conn