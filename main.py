
'''
主操作模块
用于处理网络操作，包括发送 ping 请求和从响应中提取 IP 地址。
'''

from getServiceOptimized import IPExtractor
from pingServiceOptimized import PingService
from readwriteServiceOptimized import ReadWriteService
from NslookupService import NslookupService

class NetworkOperations:
    def __init__(self, domain_list_file):
        """初始化网络操作模块。
        :param domain_list_file: 存储域名的文件路径。
        """
        self.read_write_service = ReadWriteService(domain_list_file)
        self.ping_service = PingService()
        self.nslookup_service = NslookupService()
        self.domain_list = self.read_write_service.read_txt()
        self.cname_hosts_list = []
        self.hosts_list = []

    def ping_ip_domain(self, ip_domain):
        """发送 ping 命令到指定的 IP 或域名。
        :param ip_domain: 要 ping 的 IP 或域名。
        :return: ping 命令的响应数据。
        """
        return self.ping_service.ping(ip_domain)[1]
    def nslookup_ip_domain(self, ip_domain):
        """发送 ping 命令到指定的 IP 或域名。
        :param ip_domain: 要 ping 的 IP 或域名。
        :return: ping 命令的响应数据。
        """
        return self.nslookup_service.nslookup(ip_domain)[1]

    def get_ip(self, information_str):
        """从信息字符串中提取 IP 地址。
        :param information_str: 包含 IP 地址的信息字符串。
        :return: 提取到的 IP 地址。
        """
        ip_extractor = IPExtractor(information_str)
        return ip_extractor.extract_ip()
    
    def get_domain(self, information_str):
        """从信息字符串中提取 DOMAIN 地址。
        :param information_str: 包含 DOMAIN 地址的信息字符串。
        :return: 提取到的 DOMAIN 地址。
        """
        ip_extractor = IPExtractor(information_str)
        return ip_extractor.extract_domain()

    def retrieval_ips_domains(self, ip_domain):
        """检索 IP 地址和域名，处理 CNAME 和非 CNAME 的情况。
        :param ip_domain: 要检索的 IP 或域名。
        :return: cname_hosts_list 和 hosts_list
        """
        result_ping = self.ping_ip_domain(ip_domain)
        result_nslookup = self.nslookup_ip_domain(ip_domain)
        if result_ping and result_nslookup:
            ip_address = self.get_ip(result_ping)
            domain_address_nslookup = self.get_domain(result_nslookup)
            if ip_address is not None and domain_address_nslookup:
                if ip_domain != domain_address_nslookup:
                    if f"{ip_address} {ip_domain}" not in self.cname_hosts_list:
                        self.cname_hosts_list.append(f"{ip_address} {ip_domain}")
                else:
                    if ip_address:
                        self.hosts_list.append(f"{ip_address} {ip_domain}")
        return self.cname_hosts_list, self.hosts_list

    def perform_network_operations(self):
        """执行网络操作，包括 ping 域名并提取 IP 地址，处理 CNAME 和非 CNAME 的情况。
        """
        for domain in self.domain_list:
            cname_list, host_list = self.retrieval_ips_domains(domain)
            if cname_list:
                print(f'CNAME hosts for domain {domain}: {cname_list}')
            if host_list:
                print(f'Hosts for domain {domain}: {host_list}')

# 示例用法
if __name__ == '__main__':
    ops = NetworkOperations('domain_list.txt')
    ops.perform_network_operations()
