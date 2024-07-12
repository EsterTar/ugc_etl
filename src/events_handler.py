import asyncio

import config
from clients.clickhouse_client import get_clickhouse_client

settings = config.get_settings()
logger = settings.logger

kafka_consumer_events = settings.kafka_consumer_events

clickhouse_client = get_clickhouse_client()


async def start_handler():
    while True:
        try:
            await kafka_consumer_events.start()
            while True:
                events = await kafka_consumer_events.consume_messages(batch_size=1000)
                if not events:
                    continue
                success = await clickhouse_client.save_events(events)
                if success:
                    await kafka_consumer_events.commit()
        except Exception as e:
            logger.error(f'Error occurred: {e}')
            await kafka_consumer_events.stop()
            await asyncio.sleep(10)
        finally:
            await kafka_consumer_events.stop()
