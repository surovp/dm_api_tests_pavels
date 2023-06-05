import uuid

import allure
import records
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


class DbClient:
    def __init__(self, user, password, host, database, isolation_level='AUTOCOMMIT'):
        connection_string = f'postgresql://{user}:{password}@{host}/{database}'
        self.db = records.Database(connection_string, isolation_level=isolation_level)
        self.log = structlog.get_logger(self.__class__.__name__).bind(service='db')

    def send_query(self, query):
        log = self.log.bind(event_id=str(uuid.uuid4()))
        with allure.step("Печать запроса и лога"):
            print(query)
            log.msg(
                event='request',
                query=query
            )
        with allure.step("Выполнение запроса и вывод ответа"):
            dataset = self.db.query(query=query).as_dict()
            log.msg(
                event='response',
                dataset=dataset
            )
        return dataset

    def send_bulk_query(self, query):
        log = self.log.bind(event_id=str(uuid.uuid4()))
        with allure.step("Печать запроса и лога"):
            print(query)
            log.msg(
                event='request',
                query=query
            )
        with allure.step("Выполнение запроса"):
            self.db.bulk_query(query=query)

