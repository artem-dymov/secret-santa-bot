import time
import asyncio
import psycopg2 as pg
from psycopg2.extensions import AsIs

from src.config import database_data
from src.db_api.db_models import User
from typing import Union


class DatabaseManipulator:
    def __init__(self):
        self.con = pg.connect(**database_data)
        self.con.autocommit = True
        self.cur = self.con.cursor()

        print('Connected to db')

    def __del__(self):
        self.con.close()

    def create_user(self, user_data):
        # user_data: tg_id, pib, phone_number, nv_poshta_address, ukrposhta_index
        args = [user_data['tg_id'], user_data['pib'], user_data['phone_number'], user_data['nv_poshta_address'],
                user_data['ukrposhta_index'], user_data['wishes']]
        self.cur.execute(
            'INSERT INTO users (tg_id, pib, phone_number, nv_poshta_address, ukrposhta_index, wishes) '
            'VALUES (%s, %s, %s, %s, %s, %s);', args
        )

    def find_user(self, param: dict) -> Union[User, None]:
        """
        :param param: dict with 1 pair, key - column by which you want to find one user, value - column value
        :return: user: User
        """

        self.cur.execute('SELECT * FROM users WHERE %s = %s;', [AsIs((list(param.keys())[0])),
                                                                list(param.values())[0]])
        user_data = self.cur.fetchone()
        if user_data:
            user = User(*user_data)
            return user
        else:
            return None
