'''
Created on 2024. 6. 1
@author: 0x4D
cname bypass service
'''

class cnameBypass:
    def __init__(self, target):
        self.target = f"{target}"
        self.bypass_hosts_List = []
        self.bypass_retrieval_List = []
        self.domain_creat_List = []
    
    def cname_bypass(self):
        def ping_ip_domain(ip_domain):
            from pingService import ping
            return ping(ip_domain).data
        def get_ip(information_str):
            from getService import get
            return get(information_str).data
        def bypass_retrieval(self):
            ip, domain, new_domain = self.split(' ')
            # 尝试绕过cname域名函数
            try:
                # 获取原始域名的ping结果
                new_result = ping_ip_domain(f"{new_domain}")
                # 获取拼接或缩减域名的ping结果
                if 'ms' in f"{new_result}" and 'cname' not in f"{new_result}":
                    # 判断新域名是否为cname域名
                    cname_ip = f"{ip}"[:-4]
                    # 获取原始域名的ip地址
                    new_ip = get_ip(f"{new_result}")[:-4]
                    # 获取新域名的ip地址
                    if new_ip is not None:
                        if cname_ip != new_ip:
                            # 判断新域名和原始域名ip地址是否为同一网段
                            if f"{new_ip} {domain}" not in bypass_hosts_List:
                                bypass_hosts_List.append(f"{new_ip} {domain}")
                                # 将新ip和原始域名地址写入该hosts列表
            except Exception as e:
                pass
                #print(e)
            return bypass_hosts_List
            # 返回需要改写hosts ip的列表
        # 包含cname的域名尝试绕过函数
        def domain_creat(information_str):
            ip, domain = information_str.split(' ')
            # 尝试拼接三级域名的函数
            for domain_name in domain_name_List:
                # 遍历三级域名列表
                new_domain = f"{domain_name}" + "." + f"{domain}"
                # 拼接三级域名
                # 例如：baidu.com 拼接为 www.baidu.com
                if f"{domain} {new_domain}" not in bypass_retrieval_List:
                    bypass_retrieval_List.append(f"{ip} {domain} {new_domain}")
                else:
                    pass
            #print(bypass_retrieval_List)
                    # 将原始域名和拼接域名写入该列表
        import re
        from multiprocessService import multiProcess
        from readwriteService import readWrite
        domain_name_List = readWrite("domainnamesDict.txt").read_txt()
        domain = str(self.target)
        bypass_retrieval_List = self.bypass_retrieval_List
        bypass_hosts_List = self.bypass_hosts_List
        domain_creat_List = self.domain_creat_List
        # 初始化变量
        #print(str(domain))
        try:
            retrieval_domain_Name = re.search(r'\b[^.]+\.(gov|org|cn|com|net|edu|mil|int)+.*$\b', str(domain))
            # 尝试将多级域名缩减为二级域名，并保留顶级域名（顶级域名不全，用到时加入即可）
            # 例如：www.baidu.com 缩减为 baidu.com
            new_domain = retrieval_domain_Name.group()
            if domain != new_domain:
                #print(new_domain)
                #bypass_retrieval(f"{domain}", f"{new_domain}")
                ping_info = ping_ip_domain(f"{domain}")
                ip = get_ip(f"{ping_info}")
                if f"{domain} {new_domain}" not in bypass_retrieval_List:
                    bypass_retrieval_List.append(f"{ip} {domain} {new_domain}")
                # 尝试绕过二级域名
            else:
                #print(f'{domain} 进行域名重组')
                #domain_creat(f"{domain}")
                #multiProcess(domain_creat, domain_name_List).data
                # 如果上面尝试失败，则该域名本身就为二级域名，尝试拼接为三级域名。
                ping_info = ping_ip_domain(f"{domain}")
                ip = get_ip(f"{ping_info}")
                # 获取原始域名的ip地址
                if f"{domain}" not in domain_creat_List:
                    domain_creat_List.append(f"{ip} {domain}")
        except Exception as e:
            pass
            #print(e)
        multiProcess(domain_creat, domain_creat_List).data
        #print(len(bypass_retrieval_List))
        multiProcess(bypass_retrieval, bypass_retrieval_List).data

if __name__ == '__main__':
    # 测试
    cname_domains_List = ['ywfy.gov.cn', 'oa.zju4h.com', 'org']
    def process_domain(domain):
        # 创建 cnameBypass 实例
        bypass_instance = cnameBypass(domain)
        # 调用 cname_bypass 方法
        bypass_hosts_List = bypass_instance.cname_bypass()
        return bypass_hosts_List
    
    from multiprocessService import multiProcess
    bypass_hosts_List = multiProcess(process_domain, cname_domains_List).data
    print(bypass_hosts_List)
