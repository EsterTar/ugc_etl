import json
from abc import ABC, abstractmethod
from functools import lru_cache

from clickhouse_driver import Client
import config

settings = config.get_settings()
logger = settings.logger


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

    async def save_events(self, event_data: list[dict]) -> bool:
        prepared_data = [(json.dumps(event),) for event in event_data]
        try:
            await self._client.execute(
                "INSERT INTO events (event) VALUES",
                prepared_data
            )
            return True
        except Exception as e:
            logger.error(f'Failed to save events: {e}')
            return False


@lru_cache
def get_clickhouse_client():
    client = ClickhouseClient(
        host=settings.clickhouse_host,
        user=settings.clickhouse_user,
        password=settings.clickhouse_pass
    )
    return client
