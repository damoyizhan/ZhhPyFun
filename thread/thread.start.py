# 测试daemon
import time
import threading


def threading_aaa():
    i = 0
    while True:
        print('i am in thread threading_aaa----%s' % i)
        i += 1
        time.sleep(0.19)


def threading_bbb():
    i = 0
    while True:
        i += 1
        print('i am in thread threading_bbb----%s' % i)
        time.sleep(1.21)


t1 = threading.Thread(target=threading_aaa, args=(), daemon=True)
t1.start()
t2 = threading.Thread(target=threading_bbb, args=(), daemon=True)
t2.start()

time.sleep(10)
raise Exception("AAAAAAAAAAAAAAA")
