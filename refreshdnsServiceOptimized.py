'''
Ping 服务模块
用于执行网络 Ping 操作，检查网络连通性。
'''

import subprocess
import platform

class RefreshDNSService:
    def __init__(self):
        #初始化 Ping 服务，根据操作系统选择合适的 Ping 命令。
        self.ipconfig_cmd = self._determine_ipconfig_command()

    def _determine_ipconfig_command(self):
        #根据操作系统决定使用的 Ping 命令格式
        if platform.system() == 'Windows':
            return ['ipconfig']
        else:
            return ['sudo']
    def refresh(self, target="/flushdns"):
        """执行 ipconfig或sudo 命令。
        :param target: DNS 缓存刷新命令。
        :return: 布尔值表示成功与否，以及响应结果或错误信息。
        """
        if self.ipconfig_cmd == ['sudo']:
            target = ['killall', '-HUP', 'dnsmasq']
        args = self.ipconfig_cmd + [target]
        try:
            result = subprocess.run(args, capture_output=True, text=True, check=True)
            return (result.stdout)
        except subprocess.TimeoutExpired:
            return (False, 'DNS cache refresh failed')
        except Exception as e:
            return (False, str(e))

# 示例用法
if __name__ == '__main__':
    refresh_service = RefreshDNSService()
    success = refresh_service.refresh()
    print('Refresh successful:', success)
