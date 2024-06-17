
'''
Ping 服务模块
用于执行网络 Ping 操作，检查网络连通性。
'''

import subprocess
import platform

class PingService:
    def __init__(self):
        #初始化 Ping 服务，根据操作系统选择合适的 Ping 命令。
        self.ping_cmd = self._determine_ping_command()

    def _determine_ping_command(self):
        #根据操作系统决定使用的 Ping 命令格式
        if platform.system() == 'Windows':
            return ['ping', '-n', '1']
        else:
            return ['ping', '-c', '1']

    def ping(self, target):
        """对指定目标执行 Ping 命令。
        :param target: 要 Ping 的目标地址。
        :return: 布尔值表示成功与否，以及响应结果或错误信息。
        """
        args = self.ping_cmd + [target]
        try:
            result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
            return ('time=' in result.stdout or '时间=' in result.stdout, result.stdout)
        except subprocess.TimeoutExpired:
            return (False, 'Ping request timed out')
        except Exception as e:
            return (False, str(e))

# 示例用法
if __name__ == '__main__':
    ping_service = PingService()
    success, response = ping_service.ping('www.asd.com')
    print('Ping successful:', success)
    print('Response:', response)
