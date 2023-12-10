import asyncio
from src.db_api.DatabaseSession import DatabaseSession
from src.db_api.db_models import User
from src.config import database_data


class DbManipulator:
    def __init__(self, db_session_cls=DatabaseSession, db_data=database_data):
        self.db_session_cls = db_session_cls
        self.db_data = db_data

    def create_dbs(self):
        # creates new database session
        return self.db_session_cls(self.db_data)

    async def create_user(self, user_data: dict[str]):
        """
        :param user_data: tg_id, pib, phone_number, nv_poshta_address, ukrposhta_index
        :return:
        """

        dbs = self.create_dbs()
        await asyncio.get_event_loop().run_in_executor(None, dbs.create_user, user_data)
        del dbs

    async def find_user(self, param):
        """
        :param param: dict with 1 pair, key - column by which you want to find one user, value - column value
        :return: user: User
        """

        dbs = self.create_dbs()
        user = await asyncio.get_event_loop().run_in_executor(None, dbs.find_user, param)
        del dbs

        return user

    async def delete_user(self, user_id: int) -> bool:
        """
        :param user_id: User's record id in db.
        :return: True when user deleted successfully, False if not found or error occurred
        """

        dbs = self.create_dbs()
        result = await asyncio.get_event_loop().run_in_executor(None, dbs.delete_user, user_id)
        del dbs
        return result

    async def get_all_users(self) -> list[User]:
        dbs = self.create_dbs()
        users = await asyncio.get_event_loop().run_in_executor(None, dbs.get_all_users)
        del dbs
        return users

    async def update_santa(self, user_id, santa_id) -> bool:
        """
        :param user_id:
        :param santa_id:
        :return: True when user`s santa_id updated successfully, False if not found or error occurred
        """

        dbs = self.create_dbs()
        result = await asyncio.get_event_loop().run_in_executor(None, dbs.update_santa, user_id, santa_id)
        del dbs

        if result:
            return True
        else:
            return False

    async def update_user_to_gift(self, user_id, user_to_gift_id) -> bool:
        """
        :param user_id:
        :param user_to_gift_id:
        :return: True when user`s santa_id updated successfully, False if not found or error occurred
        """

        dbs = self.create_dbs()
        result = await asyncio.get_event_loop().run_in_executor(None, dbs.update_user_to_gift,
                                                                user_id, user_to_gift_id)
        del dbs

        if result:
            return True
        else:
            return False
