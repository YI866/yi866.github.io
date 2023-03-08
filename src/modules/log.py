"""loguru使用实例

使用：

>>> from modules.log import log_console, log_file

>>> log_console.error('Logging to console ...')
>>> log_file.error('Logging to file ...')
"""

import logging
from logging import StreamHandler
from loguru import logger


logger.remove()  # 禁止默认输出到 `console`

logger.add('run.log',
           format='{time:MM-DD HH:mm:ss} [{module}] {level}: {message}',
           filter=lambda record: record['extra']['name'] == 'log_file',  # 过滤日志对象 `extra` 字段中的值，选择写入的日志文件
           rotation='10 KB',
           catch=True,
           level='INFO',
          )

logger.add(StreamHandler(),
           format='{time:MM-DD HH:mm:ss} [{module}] {level}: {message}',
           filter=lambda record: record['extra']['name'] == 'log_console',
           level='INFO',
           colorize=True
          )

log_file = logger.bind(name='log_file')
log_console = logger.bind(name='log_console')


# ************ 集成到默认logging模块 ************
class InterceptHandler(logging.Handler):
    def emit(self, record):
      logger.opt(depth=6, exception=record.exc_info).log(record.levelname, record.getMessage())

# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s %(filename)s %(levelname)s %(message)s',
#                     datefmt='%a %d %b %Y %H:%M:%S',
#                   #   filename='run.log',
#                   #   filemode='w',
#                   )

log = logging.getLogger(__name__)
log.addHandler(InterceptHandler())
log.info('xxx')
# *********************************************

