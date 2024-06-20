
'''
主操作模块
用于处理网络操作，包括发送 ping 请求和从响应中提取 IP 地址。
'''
import re
from getServiceOptimized import IPExtractor
from pingServiceOptimized import PingService
from readwriteServiceOptimized import ReadWriteService
from nslookupServiceOptimized import NslookupService
from multiprocessServiceOptimized import MultiProcessService
from accesscheckServiceOptimized import AccessCheckService
from refreshdnsServiceOptimized import RefreshDNSService
from bookMarkServiceOptimized import BookMarkService

class NetworkOperations:
    def __init__(self, domain_list_file):
        """初始化网络操作模块。
        :param domain_list_file: 存储域名的文件路径。
        """
        self.read_write_service = ReadWriteService(domain_list_file)
        self.ping_service = PingService()
        self.nslookup_service = NslookupService()
        self.refresh_service = RefreshDNSService()
        self.domain_list = self.read_write_service.read_txt()
        self.abnormal_hosts_list = []
        self.normal_hosts_list = []
        self.off_line_list = []
        self.bypass_retrieval_List = []
        self.access_list = []
        self.bypass_domain_list = []
        self.book_mark_list = []

    def ping_ip_domain(self, ip_domain):
        """发送 ping 命令到指定的 IP 或域名。
        :param ip_domain: 要 ping 的 IP 或域名。
        :return: ping 命令的响应数据。
        """
        return self.ping_service.ping(ip_domain)[1]
    def refresh_dns(self):
        """发送 ipconfig 命令。
        :param command: DNS 刷新命令。
        :return: 执行结果。
        """
        return self.refresh_service.refresh()
    def nslookup_ip_domain(self, ip_domain):
        """发送 nslookup 命令到指定的 IP 或域名。
        :param ip_domain: 要 nslookup 的 IP 或域名。
        :return: nslookup 命令的响应数据。
        """
        return self.nslookup_service.nslookup(ip_domain)

    def get_ip(self, information_str):
        """从信息字符串中提取 IP 地址。
        :param information_str: 包含 IP 地址的信息字符串。
        :return: 提取到的 IP 地址。
        """
        ip_extractor = IPExtractor(information_str)
        return ip_extractor.extract_ip()
    def domain_check(target):
        """发送 HTTP或HTTPS 请求。
        :param target: 要请求的域名。
        :return: 提取到的网站页面信息。
        """
        result = AccessCheckService(target)
        return result.check_access()
    def url_check(target):
        """发送 HTTP或HTTPS 请求。
        :param target: 要请求的URL链接。
        :return: 提取到的网站页面信息。
        """
        result = AccessCheckService(target)
        return result.access_service()
    def get_domain(self, information_str):
        """从信息字符串中提取 DOMAIN 地址。
        :param information_str: 包含 DOMAIN 地址的信息字符串。
        :return: 提取到的 DOMAIN 地址。
        """
        ip_extractor = IPExtractor(information_str)
        return ip_extractor.extract_domain()

    def retrieval_ips_domains(self, ip_domain, old_domain=None):
        """检索 IP 地址和域名，处理 CNAME 和非 CNAME 的情况。
        :param ip_domain: 要检索的 IP 或域名。
        :return: cname_hosts_list 和 hosts_list
        """
        just_ip = self.get_ip(ip_domain)
        if just_ip:
            retrieval_ip = self.ping_ip_domain(just_ip)
            if retrieval_ip and f"{just_ip} {ip_domain}" not in self.normal_hosts_list:
                self.normal_hosts_list.append(f"{just_ip} {ip_domain}")
            else:
                if f"{just_ip}" not in self.off_line_list:
                    self.off_line_list.append(f"{just_ip}")
        else:
            result_ping = self.ping_ip_domain(ip_domain)
            if result_ping:
                result_nslookup = self.nslookup_ip_domain(ip_domain)[1]
                nslookup_data = f"{result_nslookup}"
                ip_address = self.get_ip(result_ping)
                if ip_address is not None and  "名称:" in nslookup_data:
                    real_domain = re.findall(r'名称:\s+(\S+)', nslookup_data)[0]
                    if f"{ip_domain}" != real_domain and f"{ip_address}" in nslookup_data:
                        if old_domain is not None:
                            if f"{ip_address} {old_domain}" not in self.abnormal_hosts_list:
                                self.abnormal_hosts_list.append(f"{ip_address} {old_domain}")
                        else:
                            if f"{ip_address} {ip_domain}" not in self.abnormal_hosts_list:
                                self.abnormal_hosts_list.append(f"{ip_address} {ip_domain}")
                    else:
                        if old_domain is not None:
                            if f"{ip_address} {ip_domain}" not in self.normal_hosts_list:
                                self.normal_hosts_list.append(f"{ip_address} {old_domain} {ip_domain}")
                        else:
                            if f"{ip_address} {ip_domain}" not in self.normal_hosts_list:
                                self.normal_hosts_list.append(f"{ip_address} {ip_domain}")
            else:
                if f"{just_ip}" not in self.off_line_list:
                    self.off_line_list.append(f"{just_ip}")
    
    def cname_bypass(self, cname_host):
        '''
        尝试将多级域名缩减为二级域名，并保留顶级域名（顶级域名不全，用到时加入即可）
        例如: www.baidu.com 缩减为 baidu.com
        '''
        import re
        if cname_host is not None:
            ip_address, domain = cname_host.split(' ')
        try:
            retrieval_domain_Name = re.search(r'\b[^.]+\.(gov|org|cn|com|net|edu|mil|int)+.*$\b', str(domain))
            new_domain = retrieval_domain_Name.group()
            if new_domain != domain:
                self.retrieval_ips_domains(f"{new_domain}", f"{domain}")
            else:
                if f"{ip_address} {domain}" not in self.abnormal_hosts_list:
                                self.abnormal_hosts_list.append(f"{ip_address} {domain}")
        except Exception as e:
            if f"{ip_address} {domain}" not in self.abnormal_hosts_list:
                self.abnormal_hosts_list.append(f"{ip_address} {domain}")
            print(e)
    def domain_name_reconstruction(self, information_str):
        def domain_name_splicing(domain_name):
            '''
            尝试拼接三级域名的函数
            例如: baidu.com 拼接为 www.baidu.com
            '''
            new_domain = f"{domain_name}" + "." + f"{domain}"
            if f"{ip} {domain} {new_domain}" not in self.bypass_retrieval_List:
                self.bypass_retrieval_List.append(f"{ip} {domain} {new_domain}")
        '''
        尝试重构域名函数
        '''
        if information_str is not None:
            ip, domain = information_str.split(' ')
        creat_domain_name_list = ReadWriteService("domainnamesDict.txt").read_txt()
        MultiProcessService(domain_name_splicing, creat_domain_name_list).execute()
    def bypass_retrieval(self, information_str):
        # 检索cname bypass成败函数
        if information_str is not None:
            ip, domain, new_domain = information_str.split(' ')
        #print(information_str)
        # 尝试绕过cname域名函数
        try:
            # 获取原始域名的ping结果
            new_result = self.ping_ip_domain(f"{new_domain}")
            # 获取拼接或缩减域名的ping结果
            if new_result:
                nslookup_info = self.nslookup_ip_domain(f"{new_domain}")[1]
                nslookup_data = f"{nslookup_info}"
                new_ip = self.get_ip(f"{new_result}")
                if new_ip is not None:
                    cname_ip_segment = f"{ip}"[:-4]
                    new_ip_segment = f"{new_ip}"[:-4]
                    if cname_ip_segment != new_ip_segment and "名称:" in nslookup_data:
                        real_domain = re.findall(r'名称:\s+(\S+)', nslookup_data)[0]
                        if f"{new_domain}" != real_domain and f"{new_ip}" in nslookup_data:
                            if f"{ip} {domain}" not in self.abnormal_hosts_list:
                                self.abnormal_hosts_list.append(f"{ip} {domain}")
                        else:
                            if f"{new_ip} {domain}" not in self.normal_hosts_list:
                                self.normal_hosts_list.append(f"{new_ip} {domain}")
                    else:
                        if f"{ip} {domain}" not in self.abnormal_hosts_list:
                            self.abnormal_hosts_list.append(f"{ip} {domain}")
        except:
            if f"{ip} {domain}" not in self.abnormal_hosts_list:
                self.abnormal_hosts_list.append(f"{ip} {domain}")
    def perform_network_operations(self):
        """执行网络操作，包括 ping 域名并提取 IP 地址，处理 CNAME 和非 CNAME 的情况。
        """
        domain_list = self.domain_list
        print("检索 IP 地址和域名...")
        MultiProcessService(self.retrieval_ips_domains, domain_list).execute()
        print("处理 CNAME 和非 CNAME 的情况...")
        cname_hosts_list = self.abnormal_hosts_list
        hosts_list = self.normal_hosts_list
        self.abnormal_hosts_list = []
        self.normal_hosts_list = []
        print("尝试绕过cname域名...")
        MultiProcessService(self.cname_bypass, cname_hosts_list).execute()
        domain_name_reconstruction_list = self.abnormal_hosts_list
        self.bypass_retrieval_List = self.normal_hosts_list
        self.abnormal_hosts_list = []
        self.normal_hosts_list = []
        print("尝试重构域名...")
        MultiProcessService(self.domain_name_reconstruction, domain_name_reconstruction_list).execute()
        print("验证重构域名...")
        MultiProcessService(self.bypass_retrieval, self.bypass_retrieval_List).execute()
        print("尝试验证可能绕过的域名")
        for ip_domain in self.normal_hosts_list:
            ip, domain = ip_domain.split(" ")
            self.access_list.append(domain)
        original_info_list = MultiProcessService(self.domain_check, self.access_list).execute()
        try:
            ReadWriteService("C:\\Windows\\System32\\drivers\\etc\\hosts").write_txt(self.normal_hosts_list)
        except:
            ReadWriteService("hosts").write_txt(self.normal_hosts_list)
            input("hosts文件写入失败,请手动写入hosts文件并输入任意键继续...")
            pass
        print("尝试DNS刷新: ",self.refresh_dns())
        new_info_list = MultiProcessService(self.domain_check, self.access_list).execute()
        for i in range(len(new_info_list)):
            for host in self.normal_hosts_list:
                if original_info_list[i] != new_info_list[i]: 
                    self.normal_hosts_list.remove(host)
                    self.abnormal_hosts_list.append(host)
                if "None" in new_info_list[i]:
                    self.normal_hosts_list.remove(host)
                    self.abnormal_hosts_list.append(host)
        for host in self.normal_hosts_list:
            if host not in hosts_list:
                hosts_list.append(host)
        for host in hosts_list:
            ip, domain = host.split(" ")
            self.book_mark_list.append(f"{domain}")
        print("书签生成中...")
        MultiProcessService(BookMarkService.write_book_mark, self.book_mark_list).execute
        print("输出结果...")
        print("无法绕过cname域名数量: ", len(self.abnormal_hosts_list))
        print("以绕过cname域名数量: ", len(self.normal_hosts_list))
        print("正常hosts数量: ", len(hosts_list))
        print("离线域名数量: ", len(self.off_line_list))
        print("web正常访问数量: ", len(self.book_mark_list))
        ReadWriteService("cname_hosts.txt").write_txt(self.abnormal_hosts_list)
        ReadWriteService("C:\\Windows\\System32\\drivers\\etc\\hosts").write_txt(self.normal_hosts_list)
        
# 示例用法
if __name__ == '__main__':
    ops = NetworkOperations('domain_list.txt')
    ops.perform_network_operations()
