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

    def __init__(self, host: str, port: int = None):
        self._client: Client = Client(
            host=f'{host}:{port}'
        )

    async def save_events(self, event_data: str) -> bool:
        prepared_data = [(event_data,)]

        await self._client.execute(
            "INSERT INTO events (event) VALUES",
            prepared_data
        )
        return True


@lru_cache
def get_clickhouse_client():
    client = ClickhouseClient(
        host=settings.clickhouse_host
    )
    return client
