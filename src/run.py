import asyncio
from events_handler import start_handler

import config
settings = config.get_settings()


async def main():

    await settings.kafka_consumer_events.start()

    print('Starting task handler.')
    consumer_task = asyncio.create_task(start_handler())
    await consumer_task
    print('Task handler started.')


if __name__ == '__main__':
    asyncio.run(main())
