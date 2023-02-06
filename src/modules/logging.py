from loguru import logger

logger.remove()  # 禁止默认输出到 `console`
logger.add('run.log',
           format='{time:MM-DD HH:mm:ss} [{module}] {level}: {message}',
           filter=lambda x: x['extra']['name'] == 'test1',  # 过滤 `extra` 字段中的值，选择写入的日志文件
           rotation='10 KB',
           catch=True,
           level='INFO',
          )

logger_1 = logger.bind(name='test1')  # 定义 `extra` 字段
