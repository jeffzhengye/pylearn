import logging
import logging.config
from logger_examples import setup_logging

# load my module

import my_module

# load the logging configuration

logging.config.fileConfig('logging.ini')
setup_logging()

logger = logging.getLogger(__name__)
my_module.foo()
bar = my_module.Bar()
bar.bar()

logger.info('ndy')

