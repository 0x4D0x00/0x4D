
'''
IP 提取服务模块
用于从给定的文本中提取第一个有效的 IP 地址。
'''

import re

class IPExtractor:
    def __init__(self, target):
        """初始化 IP 提取器。
        :param target: 包含 IP 地址的目标文本。
        """
        self.target = target
        self.ip_pattern = re.compile(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}')  # IP 地址的正则表达式
        self.domain_pattern = re.compile(r'[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9](?:\.[a-zA-Z]{2,})+')

    def extract_ip(self):
        """从目标文本中提取 IP 地址。
        :return: 提取到的第一个 IP 地址，如果没有找到则返回 None。
        """
        match = self.ip_pattern.search(self.target)
        return match.group() if match else None
    
    def extract_domain(self):
        """从目标文本中提取域名。
        :return: 提取到的第一个域名，如果没有找到则返回 None。
        """
        match = self.domain_pattern.search(self.target)
        return match.group() if match else None

# 示例用法
if __name__ == '__main__':
    extractor = IPExtractor('Example text with IP 192.168.1.1 in it')
    ip = extractor.extract_ip()
    print('Extracted IP:', ip)
    extractor = IPExtractor('Example text with Domain example.com in it')
    domain = extractor.extract_domain()
    print('Extracted Domain:', domain)
