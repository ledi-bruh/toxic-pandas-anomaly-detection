from collections.abc import AsyncGenerator
import datetime as dt
import logging
from logging import basicConfig, getLogger, Logger
from logging.handlers import QueueHandler, QueueListener
import queue

from src.ioc import ioc
from src.shared import now
from .settings import LoggingSettings


__all__ = ['logger_plugin']


async def logger_plugin(settings: LoggingSettings) -> AsyncGenerator:
    timestamp = now().astimezone(dt.timezone(dt.timedelta(hours=+3)))

    settings.dir.mkdir(parents=True, exist_ok=True)

    log_queue = queue.Queue()
    queue_handler = QueueHandler(queue=log_queue)
    queue_listener = QueueListener(
        log_queue,
        logging.StreamHandler(),
        logging.FileHandler(
            filename=settings.dir / f'logs_{timestamp.strftime("%Y_%m_%d_%H_%M_%S")}.log',
            encoding='utf-8',
        ),
    )

    basicConfig(
        level=settings.level,
        format='[%(asctime)s] [%(levelname)s] %(message)s',
        handlers=[
            queue_handler,
        ],
    )
    logger = getLogger()

    ioc.register(Logger, instance=logger)

    queue_listener.start()

    yield

    queue_listener.stop()
