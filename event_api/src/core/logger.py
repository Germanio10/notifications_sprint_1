import sys
import logging

logger = logging.getLogger("event_api")
logger.setLevel(logging.INFO)

sh = logging.StreamHandler(sys.stdout)

formatter = logging.Formatter(
    "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
)
sh.setFormatter(formatter)

logger.addHandler(sh)
