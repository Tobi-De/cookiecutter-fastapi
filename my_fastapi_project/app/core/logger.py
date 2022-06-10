import logging

from rich.logging import RichHandler

logger = logging.getLogger(__name__)

handler = RichHandler()

logger.setLevel(logging.DEBUG)
handler.setLevel(logging.DEBUG)

handler.setFormatter(logging.Formatter("%(message)s"))

logger.addHandler(handler)
