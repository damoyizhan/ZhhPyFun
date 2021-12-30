import logging.handlers
import os
import platform


class Logger:

    @staticmethod
    def getLogger(proc_file, log_file, loglevel):

        # 兼容windows 文件路径
        if platform.system() == 'Windows':
            log_file = os.path.join(os.sep, "C:\\", log_file)

        log_directory = os.sep.join(log_file.split(os.sep)[:-1])
        if (not os.path.exists(log_directory)) or (not os.path.isdir(log_directory)):
            os.makedirs(log_directory)
        logger = logging.getLogger(proc_file)

        # 设定log level
        logger.setLevel(loglevel)

        # 添加文件输出handler，并按照时间自动分割日志文件
        file_handler = logging.handlers.TimedRotatingFileHandler(filename=log_file, when='D', interval=1, backupCount=3)
        file_handler.setFormatter(logging.Formatter("%(asctime)s-%(levelname)s-%(filename)s[%(lineno)d]-%(message)s"))
        logger.addHandler(file_handler)

        # 在windows上运行时添加控制台输出handler打印日志
        if platform.system() == 'Windows':
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(logging.Formatter("%(asctime)s-%(levelname)s-%(filename)s[%(lineno)d]-%(message)s"))
            logger.addHandler(stream_handler)

        return logger
