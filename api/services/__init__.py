import logging

httpx_logger = logging.getLogger("httpx")
httpx_logger.propagate = False
