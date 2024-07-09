from pathlib import Path
from pydantic_settings import BaseSettings
from clients.kafka_client import KafkaConsumerClient
from functools import lru_cache
from dotenv import load_dotenv
from utils.advlogger import CustomizeLogger


load_dotenv()


class Settings(BaseSettings):
    log_file_path: Path
    log_level: str
    log_format: str
    log_rotation: str
    log_retention: str
    logger: CustomizeLogger | None = None

    kafka_bootstrap_server: str
    kafka_consumer_tasks: KafkaConsumerClient | None = None
    events_topic: str

    clickhouse_host: str

    class Config:
        env_file = ".env"
        extra = "ignore"

    def setup(self):
        self.logger = CustomizeLogger.customize_logging(
            self.log_file_path,
            self.log_level,
            self.log_rotation,
            self.log_retention,
            self.log_format
        )

        self.kafka_consumer_tasks = KafkaConsumerClient(
            bootstrap_server=self.kafka_bootstrap_server,
            consumer_topic=self.events_topic,
            consumer_group=f'events',
            logger=self.logger
        )


@lru_cache(maxsize=None)
def get_settings():
    settings = Settings()
    settings.setup()
    return settings
