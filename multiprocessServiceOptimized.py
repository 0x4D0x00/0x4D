
'''
多进程服务模块
用于并行执行多个任务，提高处理效率。
'''

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
import time

class MultiProcessService():
    def __init__(self):
        """初始化多进程服务。
        :param func: 要并行执行的函数。
        :param iterable: 需要处理的数据集。
        :param max_workers: 线程池中的最大工作线程数。
        """
        super().__init__()
    def monitor_runtime(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            runtime = end_time - start_time
            print(f"{func.__name__} Runtime: {runtime:.4f} seconds")
            return result
        return wrapper
    @monitor_runtime
    def Thread_execute(self, func, iterable, max_workers=None):
        """执行并行处理网络/读写任务。
        :return: 执行结果列表。
        """
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(tqdm(executor.map(func, iterable), total=len(iterable)))
        return results
    def Thread_execute_no_tqdm(self, func, iterable, max_workers=None):
        """执行并行处理网络/读写任务。
        :return: 执行结果列表。
        """
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(func, iterable))
        return results
    def Process_execute(self, func, iterable, max_workers=2):
        """执行并行处理本地计算任务。
        :return: 执行结果列表。
        """
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            results =  list(executor.map(func, iterable))
        return results
# 示例用法
if __name__ == '__main__':
    def square(x):
        return x * x

    numbers = range(10)
    mp_service = MultiProcessService()
    results = mp_service.Thread_execute_no_tqdm(square, numbers)
    print('Squared numbers:', results)
