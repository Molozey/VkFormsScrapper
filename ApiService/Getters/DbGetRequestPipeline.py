import mysql.connector as connector
import yaml

try:
    with open("Getters/configuration.yaml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
except FileNotFoundError:
    with open("Getters/configuration.yaml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)


def get_request(query, execute_many=False):
    connection = connector.connect(host=cfg["mysql"]["host"],
                                   user=cfg["mysql"]["user"],
                                   password=cfg["mysql"]["password"],
                                   database=cfg["mysql"]["database"],
                                   ssl_disabled=True)
    cursor = connection.cursor()
    if not execute_many:
        cursor.execute(query)
        return cursor.fetchone()
    else:
        cursor.execute(query)
        return cursor.fetchall()
