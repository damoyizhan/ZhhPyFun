# -*- coding: UTF-8 -*-
# 替换原来的get logger
import logging.handlers
import platform


def getfilelogger(filename, loglevel):
    # 设置日志文件路径
    if platform.system() == 'Windows':
        __filehandler = logging.FileHandler()
    else:
        # __filehandler = logging.FileHandler(os.path.join("xxx", filename).replace('/', '\\').replace('\\', '.')[0:-3]"")
        pass

    # 设置格式
    __filehandler.setFormatter(logging.Formatter("%(asctime)s-- %(filename)s[:%(lineno)d]-%(levelname)s- %(message)s"))

    # 设置levelname
    __filehandler.setLevel(loglevel)

    # 设置logger
    __logger = logging.getLogger(filename)
    __logger.addHandler(__filehandler)
    return __logger
