import config
from clients.clickhouse_client import get_clickhouse_client

settings = config.get_settings()

kafka_consumer_events = settings.kafka_consumer_events

clickhouse_client = get_clickhouse_client()


async def start_handler():
    async for event in kafka_consumer_events.consume_message():
        await clickhouse_client.save_events(event)
