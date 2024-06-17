import subprocess
import platform
import re

def is_valid_ip(ip):
    """验证IP地址的有效性"""
    parts = ip.split('.')
    if len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
        return True
    # 处理IPv6地址
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
            return ['dig', '+short']  # 使用dig的+short选项获取简洁的IP地址输出

    def nslookup(self, target):
        try:
            args = self.nslookup_cmd + [target]
            response = subprocess.run(args, capture_output=True, text=True, timeout=1)
            output = response.stdout
            if response.returncode != 0:
                return False, f"Error executing command: {output}"
            ip_pattern = re.compile(r'名称')
            matches = ip_pattern.findall(f"{output}")
            if matches:
                return True, output
            return False, output
        except subprocess.TimeoutExpired:
            return False, "Command timed out."
        except Exception as e:
            return False, f"An error occurred: {e}"

if __name__ == '__main__':
    nslookup_service = NslookupService()
    output = nslookup_service.nslookup('www.baiducom')
    print(f"{output}")
