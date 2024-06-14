'''
Created on 2024. 6. 1
@author: 0x4D
ping service
'''
class ping:
    def __init__(self, target):
        self.target = str(target)
        self.data = self.ping_target()
    def ping_target(self):
        import platform
        import subprocess
        target = self.target
        try:
            args = ['ping', '-c', '1', target] if platform.system() == 'Linux' else ['ping', '-n', '1', target]
            result = subprocess.run(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True, timeout = 1)
            # Linux和Windows的ping命令参数不同,需要根据系统类型进行判断并执行ping IP命令
            if 'ms' in f"{result}":
                return True, result.stdout
                # 返回True, 并返回ping的报文信息
            else:
                return False
                # 返回False
        except Exception as e:
            #print(e)
            return False
            # 返回False
if __name__ == '__main__':
    target = 'www.baidu.com'
    print(ping(target).data)