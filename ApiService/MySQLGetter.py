import asyncio
import logging
import time

import mysql.connector as connector


class MySqlDaemon:
    """
    Daemon for MySQL record type.
    TODO: insert docstring
    """
    connection: connector.connection.MySQLConnection
    database_cursor: connector.connection.MySQLCursor
    table_names: list = ["FORMS_TABLE", "FORMS_DETAIL_TABLE", "USER_TABLE", "USER_ANSWERS_TABLE"]

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MySqlDaemon, cls).__new__(cls)
        return cls.instance

    def __init__(self, config):
        logging.basicConfig(
            level='INFO',
            format='%(asctime)s | %(levelname)s %(module)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        self.cfg: dict = config
        self._connect_to_database()

    def _connect_to_database(self):
        """
        Connection to MySQL database
        :return:
        """
        flag = 0
        while flag <= self.cfg["mysql"]["reconnect_max_attempts"]:
            if flag >= self.cfg["mysql"]["reconnect_max_attempts"]:
                logging.error("Cannot connect to MySQL. Reached maximum attempts")
                raise ConnectionError("Cannot connect to MySQL. Reached maximum attempts")

            try:
                self.connection = connector.connect(host=self.cfg["mysql"]["host"],
                                                    user=self.cfg["mysql"]["user"],
                                                    password=self.cfg["mysql"]["password"],
                                                    database=self.cfg["mysql"]["database"],
                                                    ssl_disabled=True)
                self.database_cursor = self.connection.cursor()
                logging.info("Success connection to MySQL database")
                return 1
            except connector.Error as e:
                flag += 1
                logging.error("Connection to database raise error: \n {error}".format(error=e))
                time.sleep(self.cfg["mysql"]["reconnect_wait_time"])

    def mysql_post_execution_handler(self, query, multi=False, input=None, need_to_commit: bool = True) -> int:
        """
        Interface to execute POST request to MySQL database
        :param query:
        :return:
        """

        flag = 0
        while flag <= self.cfg["mysql"]["reconnect_max_attempts"]:
            if flag >= self.cfg["mysql"]["reconnect_max_attempts"]:
                logging.error("Cannot connect to MySQL. Reached maximum attempts")
                raise ConnectionError("Cannot connect to MySQL. Reached maximum attempts")
            if multi:
                self.database_cursor.executemany(query, input)
                if need_to_commit:
                    self.connection.commit()
                return 1
            else:
                try:
                    self.database_cursor.execute(query)
                    if need_to_commit:
                        self.connection.commit()
                    return 1
                except connector.errors.InterfaceError as e:
                    self.database_cursor.execute(query, multi=True)
                    if need_to_commit:
                        self.connection.commit()
                    return 1
                except connector.Error as e:
                    flag += 1
                    logging.error("MySQL execution error: \n {error}".format(error=e))
                    time.sleep(self.cfg["mysql"]["reconnect_wait_time"])

    # TODO: typing
    def mysql_get_execution_handler(self, query, multi=False) -> object:
        """
        Interface to execute GET request to MySQL database
        :param query:
        :return:
        """
        flag = 0
        while flag <= self.cfg["mysql"]["reconnect_max_attempts"]:
            if flag >= self.cfg["mysql"]["reconnect_max_attempts"]:
                logging.error("Cannot connect to MySQL. Reached maximum attempts")
                raise ConnectionError("Cannot connect to MySQL. Reached maximum attempts")
            try:
                self.database_cursor.execute(query)
                return self.database_cursor.fetchall() if multi else self.database_cursor.fetchone()
            except connector.Error as e:
                flag += 1
                logging.error("MySQL execution error: \n {error}".format(error=e))
                time.sleep(self.cfg["mysql"]["reconnect_wait_time"])
