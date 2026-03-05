import logging
import json
import traceback
from datetime import datetime
from typing import Any, Dict, Optional
from pathlib import Path


class StructuredJSONFormatter(logging.Formatter):
    """
    Formats log records as JSON payloads containing required metadata
    as specified in GEMINI.md Section 18.
    """
    def format(self, record: logging.LogRecord) -> str:
        log_record: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "logger_name": record.name,
        }

        # Extract structured metadata from extra kwargs
        if hasattr(record, "run_id"):
            log_record["run_id"] = record.run_id
        if hasattr(record, "stage"):
            log_record["stage"] = record.stage
        if hasattr(record, "provider"):
            log_record["provider"] = record.provider
        if hasattr(record, "failure_class"):
            log_record["failure_class"] = record.failure_class

        if record.exc_info:
            log_record["exception"] = "".join(traceback.format_exception(*record.exc_info))

        return json.dumps(log_record)


def setup_logger(name: str = "teacher_antigravity") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Ensure logs directory exists
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # File Handler
    file_handler = logging.FileHandler(log_dir / "pipeline.log")
    file_handler.setFormatter(StructuredJSONFormatter())
    logger.addHandler(file_handler)

    # Console Handler for development
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(StructuredJSONFormatter())
    logger.addHandler(console_handler)

    return logger


logger = setup_logger()
