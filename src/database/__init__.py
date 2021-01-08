import sqlite3
from typing import Iterable

_create_sql = """
    CREATE TABLE IF NOT EXISTS black_list(
        id INTEGER PRIMARY KEY,
        reason TEXT,
        datetime TEXT
    )
    """
_insert_sql = """
    INSERT OR IGNORE INTO black_list
    (id, reason, datetime) VALUES (?,?,datetime('now', 'localtime'))
"""


class BlackListDb:

    def __init__(self, file):
        self._conn = sqlite3.connect(file)
        self._conn.execute(_create_sql)
        self._conn.commit()

    def __del__(self):
        self._conn.close()

    def add_person(self, ids: Iterable[int], reason):
        params = map(lambda x: [x, reason], ids)
        try:
            self._conn.executemany(_insert_sql, params)
            self._conn.commit()
        except sqlite3.Error as err:
            print("DbService: unable to insert person id=%d" % id, err)

    def select_person(self, id):
        try:
            cursor = self._conn.cursor()
            cursor.execute("""
                SELECT * FROM black_list
                WHERE id = ? 
            """, [id])
            res = cursor.fetchone()
            cursor.close()
        except sqlite3.Error as err:
            print("DbService: unable to select person with id=%d" % id, err)
        return res

    def select_all_ids(self):
        """
        :return: The set of blocked ids
        """
        curs = self._conn.execute("""
            SELECT id FROM black_list
        """)
        result = curs.fetchall()
        curs.close()
        return set(map(lambda x: x[0], result))

    def count(self):
        curs = self._conn.execute("""
            SELECT COUNT(*) FROM black_list
        """)
        return curs.fetchone()[0]
