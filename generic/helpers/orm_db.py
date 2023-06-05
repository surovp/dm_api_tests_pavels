from sqlalchemy import select, delete, update
from generic.helpers.orm_models import User
from orm_client.orm_client import OrmClient
from typing import List
import allure


class OrmDatabase:
    def __init__(self, user, password, host, database):
        self.db = OrmClient(user, password, host, database)

    def get_all_users(self):
        query = select([User])
        with allure.step("Получаем через БД всех пользователей"):
            dataset = self.db.send_query(query)
        return dataset

    def get_user_by_login(self, login) -> List[User]:
        query = select([User]).where(
            User.Login == login
        )
        with allure.step("Получаем через БД пользователя по логину"):
            dataset = self.db.send_query(query)
        return dataset

    def delete_user_by_login(self, login):
        query = delete(User).where(
            User.Login == login
        )
        with allure.step("Удаляем в БД пользователя по логину"):
            dataset = self.db.send_bulk_query(query)
        return dataset

    def activate_user(self, login, is_activate: bool = True):

        query = update(User).where(
            User.Login == login
        ).values(
            {
                User.Activated: is_activate
            }
        )
        with allure.step("Активируем пользователя через БД"):
            dataset = self.db.send_bulk_query(query)
        return dataset


