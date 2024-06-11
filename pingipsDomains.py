'''
ping ip 或 域名, 返回在线ip
'''
import re
import platform
import subprocess
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def get_ip(infomation_str):
    try:
        ip_address = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', str(infomation_str))   # 提取ip地址
        ip_address = ip_address.group()
        return str(ip_address)
    except Exception as e:
        #print(e)
        return None
def ping_ip_domain(ip_domain):
    # 发送ping命令
    try:
        Linux_args = ['ping', '-c', '1', ip_domain]
        Windows_args = ['ping', '-n', '1', ip_domain]
        result = subprocess.run(Linux_args if platform.system() == 'Linux' else Windows_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=1)
        if 'ms' in str(result):
            return True, str(result)
        else:
            if ip_domain not in off_line_List:
                off_line_List.append(ip_domain)
            return False
    except Exception as e:
        #print(e)
        return False
def retrieval_ips_domains(ip_domain):
    result = ping_ip_domain(ip_domain)
    if result:
        ip_address = get_ip(str(result))
        if ip_address is not None:
            if 'cname' in str(result):
                if f"{ip_address} {ip_domain}" not in cname_hosts_List:
                    cname_hosts_List.append(f"{ip_address} {ip_domain}")
            else: 
                if ip_address:
                    hosts_List.append(f"{ip_address} {ip_domain}")
    return cname_hosts_List, hosts_List
def cname_bypass(domain):
    def bypass_retrieval(domain, new_domain):
        try:
            old_result = ping_ip_domain(str(domain))
            new_result = ping_ip_domain(str(new_domain))
            if 'ms' in str(new_result) and 'cname' not in str(new_result):
                cname_ip = get_ip(str(old_result))
                new_ip = get_ip(str(new_result))
                if new_ip is not None:
                    x = re.search(r'[0-9]{1,3}\.', str(cname_ip))
                    x = x.group()[:-1]
                    y = re.search(r'[0-9]{1,3}\.', str(new_ip))
                    y = y.group()[:-1]
                    if int(x) != int(y):
                        if f"{new_ip} {domain}" not in bypass_hosts_List:
                            bypass_hosts_List.append(f"{new_ip} {domain}")
        except Exception as e:
            print(e)
        return bypass_hosts_List
    def domain_creat(domain):
        for domain_name in domain_name_List:
            new_domain = f"{domain_name}" + "." + f"{domain}"
            bypass_retrieval(domain, new_domain)
    #__main__
    try:
        retrieval_domain_Name = re.search(r'\b[^.]+\.(?:gov|cn|com)+.*$', str(domain))
        if retrieval_domain_Name:
            new_domain = retrieval_domain_Name.group()[1:]
            bypass_retrieval(str(domain), str(new_domain))
        else:
            #print(f'{domain} 进行域名重组')
            domain_creat(str(domain))
    except Exception as e:
        domain_creat(str(domain))
        print(e)
def multithreaded_processor(func, iterable):
    
    with ThreadPoolExecutor() as executor:
        for result in tqdm(executor.map(func, iterable), total=len(iterable)):
            pass

if __name__ == '__main__':
    try:
        with open('ipsDomains.txt', 'r') as file:
            ips_domains_List = list(set(line.strip() for line in file if line.strip()))
    except Exception as e:
        print(e)
        with open('ipsDomains.txt', 'w') as file:
            pass
        ips_domains_List = []
        print('ipsDomains.txt文件内容为空。')
    on_line_List = []
    on_line_ip_List = []
    on_line_domain_List = []
    off_line_List = []
    cname_ips_List = []
    cname_hosts_List = []
    bypass_hosts_List = []
    hosts_List = []
    cname_domain_List = []
    bypass_domain_List = []
    print("ping ips and domains")
    multithreaded_processor(retrieval_ips_domains, ips_domains_List)
    try:
        with open("domainnamesDict.txt", 'r') as file:  # 读取域名字典
            domain_name_List = list(set(line.strip() for line in file if line.strip()))
    except Exception as e:
        print(e)
        domain_name_List = []
    print("bypass cname domains")
    for ip_domain in cname_hosts_List:
        ip, domain = ip_domain.split(' ')
        cname_ips_List.append(ip)
        cname_domain_List.append(domain)
    print(cname_domain_List)
    multithreaded_processor(cname_bypass, cname_domain_List)

    if bypass_hosts_List is not None:
        with open('C:\\Windows\\System32\\drivers\\etc\\hosts', 'w') as file:   # 改写hosts文件，使用真实ip与域名绑定
            file.write('\n'.join(bypass_hosts_List))

    for ip_domain in bypass_hosts_List:
        ip, domain = ip_domain.split(' ')
        if f"{ip} {domain}" not in hosts_List:
            hosts_List.append(f"{ip} {domain}")
    with open('hosts.txt', 'w') as file:
        file.write('\n'.join(hosts_List))
    
    for ip_domain in hosts_List:
        ip, domain = ip_domain.split(' ')
        on_line_ip_List.append(ip)
        on_line_domain_List.append(domain)
    with open('onlineIPs.txt', 'w') as file:
        file.write('\n'.join(on_line_ip_List))
    with open('onlineDomains.txt', 'w') as file:
        file.write('\n'.join(on_line_domain_List))

    print(f"on line ips:{len(hosts_List)}")
    print(f"off line ips:{len(off_line_List)}")
    print(f"cname domains:{len(cname_hosts_List)}")
    print(f"bypass cname数量:{len(bypass_hosts_List)}")
    print("任务执行完成")
