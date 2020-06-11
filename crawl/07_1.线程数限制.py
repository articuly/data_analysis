# -*- coding=utf-8 -*-
from threading import Thread, current_thread, active_count, Lock
import time, random
import os

print(os.getpid())
lists = list(range(100000))
lock = Lock()


def run_thread():
    print(current_thread().getName())
    time.sleep(random.random())
    lock.acquire()
    try:
        if len(lists) > 0:
            lists.pop()
    except Exception:
        pass
    finally:
        lock.release()


# 不加限制的情况下线程数会达到一个最大值
# 并不是线程越多性能越好
t_start = time.time()
thread_list = []
while len(lists) > 0:
    t = Thread(target=run_thread)
    t.start()
    thread_list.append(t)
    print("当前活跃线程数", active_count())

# 等待所有线程结束，才计算结束的时间
for t in thread_list:
    t.join()

t_end = time.time()
print("耗时:", t_end - t_start)
