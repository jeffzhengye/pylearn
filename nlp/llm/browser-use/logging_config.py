# browser_use/logging_config.py
import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()

def addLoggingLevel(levelName, levelNum, methodName=None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.
    ...
    """
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
        raise AttributeError('{} already defined in logging module'.format(levelName))
    if hasattr(logging, methodName):
        raise AttributeError('{} already defined in logging module'.format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
        raise AttributeError('{} already defined in logger class'.format(methodName))

    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)

def setup_logging(verbose: bool = False):
    # Try to add RESULT level, but ignore if it already exists
    try:
        addLoggingLevel('RESULT', 35)  # This allows ERROR, FATAL and CRITICAL
    except AttributeError:
        pass  # Level already exists, which is fine

    # Check if handlers are already set up
    if logging.getLogger().hasHandlers():
        return

    # Clear existing handlers
    root = logging.getLogger()
    root.handlers = []

    class BrowserUseFormatter(logging.Formatter):
        def format(self, record):
            if type(record.name) == str and record.name.startswith('browser_use.'):
                record.name = record.name.split('.')[-2]
            return super().format(record)

    # Setup single handler for all loggers
    console = logging.StreamHandler(sys.stdout)

    if verbose:
        root.setLevel(logging.DEBUG)
        console.setLevel(logging.DEBUG)
        console.setFormatter(BrowserUseFormatter('%(levelname)-8s [%(name)s] %(message)s'))
    else:
        root.setLevel(logging.INFO)
        console.setLevel(logging.INFO)
        console.setFormatter(BrowserUseFormatter('%(message)s'))

    # Configure root logger only
    root.addHandler(console)

    # Configure browser_use logger
    browser_use_logger = logging.getLogger('browser_use')
    browser_use_logger.propagate = False  # Don't propagate to root logger
    browser_use_logger.addHandler(console)
    browser_use_logger.setLevel(root.level)  # Set same level as root logger

    logger = logging.getLogger('browser_use')
    logger.info('BrowserUse logging setup complete with verbose: %s', verbose)

    # Silence third-party loggers
    for logger in [
        'WDM',
        'httpx',
        'selenium',
        'playwright',
        'urllib3',
        'asyncio',
        'langchain',
        'openai',
        'httpcore',
        'charset_normalizer',
        'anthropic._base_client',
        'PIL.PngImagePlugin',
        'trafilatura.htmlprocessing',
        'trafilatura',
    ]:
        third_party = logging.getLogger(logger)
        third_party.setLevel(logging.ERROR)
        third_party.propagate = False