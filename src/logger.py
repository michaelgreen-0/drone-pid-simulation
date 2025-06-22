import logging
import sys
from pythonjsonlogger import json
from datetime import datetime


class CustomJsonFormatter(json.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record["timestamp"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        log_record["level"] = record.levelname


class Logger:
    def __init__(self):
        self.logger = logging.getLogger("drone_simulation_logger")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            log_handler = logging.StreamHandler(sys.stdout)
            log_handler.setFormatter(CustomJsonFormatter())
            self.logger.addHandler(log_handler)

    def info(self, msg, extra=None):
        if extra is None:
            extra = {}
        self.logger.info(msg, extra=extra)
