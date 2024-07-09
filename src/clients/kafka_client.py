import asyncio
import json
import time

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError


class KafkaConsumerClient:

    def __init__(
            self,
            consumer_topic: str,
            bootstrap_server: str,
            consumer_group: str,
            logger
    ):
        self._consumer_topic: str = consumer_topic
        self._consumer_group: str = consumer_group
        self._bootstrap_server: str = bootstrap_server
        self._consumer = None
        self._logger = logger

    async def start(self):
        if self._consumer:
            return
        self._logger.info('Starting consumer.')
        attempts_count = 10
        for attempt in range(0, attempts_count):
            try:
                self._consumer = AIOKafkaConsumer(
                    self._consumer_topic,
                    bootstrap_servers=self._bootstrap_server,
                    group_id=self._consumer_group,
                    auto_offset_reset='earliest'
                )
                await self._consumer.start()
            except KafkaConnectionError as connection_error:
                if attempt == attempts_count - 1:
                    raise connection_error
                await asyncio.sleep(10)
        self._logger.info('Consumer started.')

    async def stop(self):
        self._logger.info('Stopping consumer.')
        await self._consumer.stop()
        self._logger.info('Consumer stopped.')

    async def consume_message(self):
        async for msg in self._consumer:
            key = msg.key.decode('utf-8') if msg.key else None
            value = msg.value.decode('utf-8') if msg.value else None
            data = json.loads(value)
            self._logger.info(f'Message consumed. Key: {key}. Data: {data}.')
            yield data
