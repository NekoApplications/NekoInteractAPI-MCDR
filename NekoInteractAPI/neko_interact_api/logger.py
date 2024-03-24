import logging
from mcdreforged.utils.logger import MCDReforgedLogger

logger: MCDReforgedLogger = None

def update_logger(loggger):
    global logger
    logger = loggger