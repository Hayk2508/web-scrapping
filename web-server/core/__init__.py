from loguru import logger
from core.settings import DEBUG


logger.remove()
if DEBUG:
    logger.add(
        "parser_log.log",
        format="{time:YYYY-MM-DD HH:mm:ss} {level} {message} {extra} {exception}",
        level="DEBUG",
        enqueue=True,
        backtrace=True,
        diagnose=False,
    )
else:
    logger.add(
        "parser_log.log",
        rotation="50 MB",
        format="{time:YYYY-MM-DD HH:mm:ss} {level} {message} {extra} {exception}",
        level="INFO",
        enqueue=True,
        backtrace=True,
        diagnose=False,
        compression="zip",
    )
