import json
from abc import ABC, abstractmethod
from functools import lru_cache

from clickhouse_driver import Client
import config

settings = config.get_settings()


class ClickhouseClientBase(ABC):

    @abstractmethod
    async def save_events(self, data: list[dict]) -> bool:
        pass


class ClickhouseClient(ClickhouseClientBase):

    def __init__(self, host: str, user: str, password: str):
        self._client: Client = Client(
            host=f'{host}',
            user=user,
            password=password
        )

    async def save_events(self, event_data: dict) -> bool:
        prepared_data = [(json.dumps(event_data),)]

        self._client.execute(
            "INSERT INTO events (event) VALUES",
            prepared_data
        )
        return True


@lru_cache
def get_clickhouse_client():
    client = ClickhouseClient(
        host=settings.clickhouse_host,
        user=settings.clickhouse_user,
        password=settings.clickhouse_pass
    )
    return client
