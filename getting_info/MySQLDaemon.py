import asyncio
import logging
import time

import mysql.connector as connector
from dbDeployCmd import create_tables_query


class MySqlDaemon:
    """
    Daemon for MySQL record type.
    TODO: insert docstring
    """
    connection: connector.connection.MySQLConnection
    database_cursor: connector.connection.MySQLCursor
    table_names: list = ["FORMS_TABLE", "FORMS_DETAIL_TABLE", "USER_TABLE", "USER_ANSWERS_TABLE"]

    def __init__(self, config):
        logging.basicConfig(
            level='INFO',
            format='%(asctime)s | %(levelname)s %(module)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        self.cfg: dict = config
        self._connect_to_database()

        self._create_not_exist_database()

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
                                                    database=self.cfg["mysql"]["database"])
                self.database_cursor = self.connection.cursor()
                logging.info("Success connection to MySQL database")
                return 1
            except connector.Error as e:
                flag += 1
                logging.error("Connection to database raise error: \n {error}".format(error=e))
                time.sleep(self.cfg["mysql"]["reconnect_wait_time"])

    def _mysql_post_execution_handler(self, query, need_to_commit: bool = False) -> int:
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
    def _mysql_get_execution_handler(self, query) -> object:
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
                return self.database_cursor.fetchone()
            except connector.Error as e:
                flag += 1
                logging.error("MySQL execution error: \n {error}".format(error=e))
                time.sleep(self.cfg["mysql"]["reconnect_wait_time"])

    def _create_not_exist_database(self):
        """
        Check if all need tables are exiting. If not creates them.
        :return:
        """
        """
        Check if all need tables are exiting. If not creates them.
        :return:
        """
        _all_exist = True
        _query = """SHOW TABLES LIKE '{}'"""
        for table_name in self.table_names:
            result = self._mysql_get_execution_handler(_query.format(table_name))
            if not result:
                logging.warning(f"Table {table_name} NOT exist; Start creating...")
                self._mysql_post_execution_handler(
                    create_tables_query)
                _all_exist = False

        if _all_exist:
            logging.info("All need tables already exists. That's good!")
