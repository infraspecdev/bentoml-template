"""
This module configures the structure logging setup using structlog.
"""

import os
import logging
from dotenv import load_dotenv
import structlog
import orjson

load_dotenv()

level = os.getenv("LOG_LEVEL", "WARNING").upper()
LOG_LEVEL = getattr(logging, level, logging.WARNING)


def configure_structure_logging():
    """
    Configure structure logging with structlog.
    """
    structlog.configure(
        cache_logger_on_first_use=True,
        wrapper_class=structlog.make_filtering_bound_logger(LOG_LEVEL),
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.format_exc_info,
            structlog.processors.EventRenamer("message"),
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.JSONRenderer(serializer=orjson.dumps),
        ],
        logger_factory=structlog.BytesLoggerFactory(),
    )


logger = structlog.get_logger()
