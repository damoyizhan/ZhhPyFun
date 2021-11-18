# -*- coding: UTF-8 -*-
# 使用 threading.enumerate() 枚举被进程调起的所有线程

import threading
import time


def run():
    for i in range(1, 100):
        print("SubThread")
        print(i)
        time.sleep(1)
        if i == 100:
            raise Exception("子线程执行完成退出")


if __name__ == '__main__':

    print("MainThread")

    sub_threading = threading.Thread(target=run, name='Consumer-Thread-0', daemon=True, args=())

    sub_threading.start()
    xx = 0
    try:
        while True:
            for t in threading.enumerate():
                print("==========================")
                print(t.__dict__)
                print("==========================")
            time.sleep(1.11)
            xx = xx + 1

            if xx == 10:
                raise Exception("MMMMMMMM")
    except Exception as e:

        for t in threading.enumerate():
            print("exception %s" % t.__dict__)
