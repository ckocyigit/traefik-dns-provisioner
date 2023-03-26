import logging
from logging.handlers import RotatingFileHandler
import coloredlogs

class DuplicateFilter(logging.Filter):

    def filter(self, record):
        # add other fields if you need more granular comparison, depends on your app
        current_log = (record.module, record.levelno, record.msg)
        if current_log != getattr(self, "last_log", None):
            self.last_log = current_log
            return True
        return False

LOG_FILENAME = "dnsupdater.log"
logger = logging.getLogger("dnsupdater")
handler = RotatingFileHandler(
    LOG_FILENAME, maxBytes=10_000_000, backupCount=5, encoding="utf-8"
)
handler.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addFilter(DuplicateFilter())

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler("dnsupdater-DEBUG.log", "w", "utf-8")],
)
coloredlogs.install(fmt="%(asctime)s %(message)s", logger=logger)

def appLogger():
    return logger