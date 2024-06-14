'''
Created on 2024. 6. 1
@author: 0x4D
multi process service
'''
class multiProcess:
    def __init__(self, function, iterable):
        self.function = function
        self.iterable = list(iterable)
        self.data = self.distribute_tasks()
        
    def distribute_tasks(self):
        import concurrent.futures
        from tqdm import tqdm
        function = self.function
        iterable = self.iterable
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 多线程分发任务func = 需要调用的函数名，iterable = func该函数需要用到的列表
        #with concurrent.futures.ThreadPoolExecutor(max_workers=x) as executor:   # 设置最大线程数为x, x为整数，范围为1-100，如果有资源限制，请设置为大于0小于等于100的整数。
            result = list(tqdm(executor.map(function, iterable), total=len(iterable)))
            # 显示进度条
            return result
if __name__ == '__main__':
    def get_ip(information_str):
        from getService import get
        return get(information_str).data
    my_list = ['asd 111.111.111.111 asd', ' asd 222.222.222.222 asd ', ' gasf333.333.333.333', 'fqwe 444.444.444.444'
                , '555.555.555.555 asd', '666.666.666.666gfqe', '777.777.777.777gdsa', 'asdf888.888.888.888']
    print(multiProcess(get_ip, my_list).data)
