
'''
多进程服务模块
用于并行执行多个任务，提高处理效率。
'''

from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

class MultiProcessService:
    def __init__(self, function, iterable):
        """初始化多进程服务。
        :param function: 要并行执行的函数。
        :param iterable: 需要处理的数据集。
        :param max_workers: 线程池中的最大工作线程数。
        """
        self.function = function
        self.iterable = iterable
        self.data = self.execute()
    def execute(self):
        """执行并行处理任务。
        :return: 执行结果列表。
        """
        with ThreadPoolExecutor() as executor:
            results = list(tqdm(executor.map(self.function, self.iterable), total=len(self.iterable)))
        return results

# 示例用法
if __name__ == '__main__':
    def square(x):
        return x * x

    numbers = range(10)
    mp_service = MultiProcessService(square, numbers)
    results = mp_service.execute()
    print('Squared numbers:', results)
