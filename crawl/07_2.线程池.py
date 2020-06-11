# -*- coding=utf-8 -*-

from concurrent.futures import ThreadPoolExecutor, as_completed, wait, ALL_COMPLETED
from threading import active_count, current_thread, Lock
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
            print(lists.pop())

    except Exception as e:
        print(e)
    finally:
        lock.release()


t_start = time.time()
# 单线程 run_thread()
# 线程持可以限制线程数量
# 通过线程池，不再通过创建新的线程处理任务，而是在已经创建的线程里处理数据
max_threads = 2000
executor = ThreadPoolExecutor(max_workers=max_threads)
# 运行10万次弹出列表的线程
# 线程数总是控制在max内，当线程数达到max后，会等待线程释放
# 线程释放后会被重新激活
threads = {executor.submit(run_thread): i for i in range(0, 100000)}

t_start_1 = time.time()
wait(threads, return_when=ALL_COMPLETED)
t_end = time.time()
print("线程耗时:", t_end - t_start_1)
t_end = time.time()
print(lists)
print("全部耗时:", t_end - t_start)
