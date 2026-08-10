import logging
import json
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    def format(self, record):
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(entry)


def setup_logging():
    logger = logging.getLogger("sentinel")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler("sentinel.log", encoding="utf-8")
    file_handler.setFormatter(JsonFormatter())

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(JsonFormatter())

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


def count_errors(path: str = "sentinel.log") -> int:
    count = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
                if entry.get("level") == "ERROR":
                    count += 1
            except json.JSONDecodeError:
                continue
    return count
