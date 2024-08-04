from collections.abc import Callable
import threading
from typing import Any, Iterable, Mapping
import logging

logger = logging.getLogger(__name__)

class EmailThreading(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        try:
            self.email_message.send()
        except Exception as e:
            logger.error(f"Failed to send email: {e}")