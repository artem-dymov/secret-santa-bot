import time
import asyncio
import psycopg2 as pg
from psycopg2.extensions import AsIs

from src.db_api.db_models import User
from typing import Union


class DatabaseSession:
    def __init__(self, db_data):
        self.con = pg.connect(**db_data)
        self.con.autocommit = True
        self.cur = self.con.cursor()

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

    def delete_user(self, user_id: int) -> bool:
        """
        :param user_id: User's record id in db.
        :return: True when user deleted successfully, False if not found or error occurred
        """

        try:
            self.cur.execute('DELETE FROM users WHERE id = %s;', [user_id])
            return True
        except Exception as e:
            print(e)
            return False

    def get_all_users(self) -> list[User]:
        self.cur.execute('SELECT * FROM users')
        users_raw = self.cur.fetchall()
        users = []

        for user_raw in users_raw:
            users.append(User(*user_raw))

        return users

    def update_santa(self, user_id, santa_id) -> bool:
        """
        :param user_id:
        :param santa_id:
        :return: True when user`s santa_id updated successfully, False if not found or error occurred
        """
        try:
            self.cur.execute('UPDATE users SET santa_id = %s WHERE id = %s', [santa_id, user_id])
            return True
        except Exception as e:
            print(e)
            return False

    def update_user_to_gift(self, user_id, user_to_gift_id) -> bool:
        """
        :param user_id:
        :param user_to_gift_id:
        :return: True when user`s santa_id updated successfully, False if not found or error occurred
        """
        try:
            self.cur.execute('UPDATE users SET user_to_gift_id = %s WHERE id = %s',
                             [user_to_gift_id, user_id])
            return True
        except Exception as e:
            print(e)
            return False

