import subprocess
import platform
import re

def is_valid_ip(ip):
    """验证IP地址的有效性"""
    parts = ip.split('.')
    if len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
        return True
    try:
        from ipaddress import ip_address
        ip_address(ip)
        return True
    except ValueError:
        return False

class NslookupService:
    def __init__(self):
        self.nslookup_cmd = self._determine_nslookup_command()

    def _determine_nslookup_command(self):
        if platform.system() == 'Windows':
            return ['nslookup']
        else:
            return ['dig', '+short']

    def nslookup(self, target):
        try:
            args = self.nslookup_cmd + [target]
            response = subprocess.run(args, capture_output=True, text=True, timeout=1)
            output = response.stdout.strip()  # 去除输出字符串的空白字符
            if response.returncode != 0:
                return False, f"Error executing command: {output}"
            
            # 根据操作系统和命令类型使用不同的正则表达式来提取IP地址
            if platform.system() == 'Windows':
                ip_pattern = re.compile(r'名称')
            else:
                ip_pattern = re.compile(r'^\S+$')  # 对于dig +short，还未调整

            matches = ip_pattern.search(output)
            if matches:
                return True, output
            else:
                return False, "False"
        except subprocess.TimeoutExpired:
            return False, "Command timed out."
        except Exception as e:
            return False, f"An error occurred: {e}"

if __name__ == '__main__':
    nslookup_service = NslookupService()
    output = nslookup_service.nslookup('www.baidu.com')
    print(f"Result: {output[0]}, Info: {output[1]}")  # 格式化输出
