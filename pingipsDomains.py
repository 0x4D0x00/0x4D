'''
ping ip 或 域名, 返回在线ip
'''
import re
import platform
import subprocess
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def get_ip(infomation_str):
    # 提取ip地址函数
    try:
        ip_address = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', str(infomation_str))
        ip_address = ip_address.group()
        # 提取ip地址
        return str(ip_address)
        # 返回ip地址
    except Exception as e:
        #print(e)
        return None
        # 返回None
def ping_ip_domain(ip_domain):
    # 发送ping命令获取ping的报文信息函数
    try:
        Linux_args = ['ping', '-c', '1', ip_domain]
        Windows_args = ['ping', '-n', '1', ip_domain]
        result = subprocess.run(Linux_args if platform.system() == 'Linux' else Windows_args, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True, timeout = 1)
        # Linux和Windows的ping命令参数不同，需要根据系统类型进行判断并执行ping IP命令
        if 'ms' in str(result):
            return True, str(result)
            # 返回True, 并返回ping的报文信息
        else:
            if ip_domain not in off_line_List:
                off_line_List.append(ip_domain)
            return False
            # 返回False并将该地址添加到离线地址列表中
    except Exception as e:
        #print(e)
        return False
def retrieval_ips_domains(ip_domain):
    # 检索ip地址和域名函数
    result = ping_ip_domain(ip_domain)
    # 发送ping命令获取ping的报文信息
    if result:
        ip_address = get_ip(str(result))
        # 提取ip地址
        if ip_address is not None:
            if 'cname' in str(result):
                # 判断是否存在cname
                if f"{ip_address} {ip_domain}" not in cname_hosts_List:
                    cname_hosts_List.append(f"{ip_address} {ip_domain}")
            else: 
                if ip_address:
                    hosts_List.append(f"{ip_address} {ip_domain}")
                    # 不包含cname地址则加入hosts列表中
    return cname_hosts_List, hosts_List
    # 返回hosts列表和包含cname的hosts列表
def cname_bypass(domain):
    # 包含cname的域名尝试绕过函数
    def bypass_retrieval(domain, new_domain):
        # 尝试绕过cname域名函数
        try:
            old_result = ping_ip_domain(str(domain))
            # 获取原始域名的ping结果
            new_result = ping_ip_domain(str(new_domain))
            # 获取拼接或缩减域名的ping结果
            if 'ms' in str(new_result) and 'cname' not in str(new_result):
                # 判断新域名是否为cname域名
                cname_ip = get_ip(str(old_result))
                # 获取原始域名的ip地址
                new_ip = get_ip(str(new_result))
                # 获取新域名的ip地址
                if new_ip is not None:
                    x = re.search(r'[0-9]{1,3}\.', str(cname_ip))
                    x = x.group()[:-1]
                    y = re.search(r'[0-9]{1,3}\.', str(new_ip))
                    y = y.group()[:-1]
                    if int(x) != int(y):
                        # 判断新域名和原始域名ip地址是否为同一网段
                        if f"{new_ip} {domain}" not in bypass_hosts_List:
                            bypass_hosts_List.append(f"{new_ip} {domain}")
                            # 将新ip和原始域名地址写入该hosts列表
        except Exception as e:
            print(e)
        return bypass_hosts_List
        # 返回需要改写hosts ip的列表
    def domain_creat(domain):
        # 尝试拼接三级域名的函数
        for domain_name in domain_name_List:
            # 遍历三级域名词典列表
            new_domain = f"{domain_name}" + "." + f"{domain}"
            # 拼接三级域名
            # 例如：baidu.com 拼接为 www.baidu.com
            bypass_retrieval(domain, new_domain)
            # 尝试使用拼接的三级域名
    # 函数由此执行
    try:
        retrieval_domain_Name = re.search(r'\b[^.]+\.(?:gov|org|cn|com|net|edu|mil|int)+.*$\b', str(domain))
        # 尝试将多级域名缩减为二级域名，并保留顶级域名（顶级域名不全，用到时加入即可）
        # 例如：www.baidu.com 缩减为 baidu.com
        if retrieval_domain_Name:
            new_domain = retrieval_domain_Name.group()[1:]
            bypass_retrieval(str(domain), str(new_domain))
            # 尝试绕过二级域名
        else:
            #print(f'{domain} 进行域名重组')
            domain_creat(str(domain))
            # 如果上面尝试失败，则该域名本身就为二级域名，尝试拼接为三级域名。
    except Exception as e:
        domain_creat(str(domain))
        print(e)
def multithreaded_processor(func, iterable):
    with ThreadPoolExecutor() as executor:
        # 多线程分发任务func = 需要调用的函数名，iterable = func该函数需要用到的列表
    #with ThreadPoolExecutor(max_workers=x) as executor:   # 设置最大线程数为x, x为整数，范围为1-100，如果有资源限制，请设置为大于0小于等于100的整数。
        for result in tqdm(executor.map(func, iterable), total=len(iterable)):
            # 显示进度条
            pass
            # 返回结果

if __name__ == '__main__':
    try:
        with open('ipsDomains.txt', 'r') as file:
            ips_domains_List = list(set(line.strip() for line in file if line.strip()))
            # 尝试读取ip和域名文件，并去重后加入列表
    except Exception as e:
        print(e)
        with open('ipsDomains.txt', 'w') as file:
            pass
        ips_domains_List = []
        # 如果文件不存在，则创建一个空文件和空列表。
        print('ipsDomains.txt文件内容为空。')
    print(len(ips_domains_List))
    # 创建任务所需的列表
    on_line_List = []   # 在线的ip和域名列表
    on_line_ip_List = []    # 在线的ip列表
    on_line_domain_List = []    # 在线的域名列表
    off_line_List = []   # 离线的ip和域名列表
    hosts_List = [] # 存活的hosts列表
    cname_ips_List = [] # 存在cname的ip列表
    cname_domain_List = []  # 存在cname的域名列表
    cname_hosts_List = []   # 存在cname的hosts列表
    bypass_hosts_List = []  # 需要改写的hosts列表
    bypass_domain_List = []  # 需要bypass的域名列表
    print("ping ips and domains")
    multithreaded_processor(retrieval_ips_domains, ips_domains_List)
    # 多线程检索ip和域名列表
    try:
        with open("domainnamesDict.txt", 'r') as file:
            domain_name_List = list(set(line.strip() for line in file if line.strip()))
            # 尝试读取三级域名词典文件，并去重后加入列表
    except Exception as e:
        print(e)
        domain_name_List = []
        # 如果文件不存在，则创建一个空文件和空列表。
    print("bypass cname domains")
    for ip_domain in cname_hosts_List:
        ip, domain = ip_domain.split(' ')
        cname_ips_List.append(ip)
        cname_domain_List.append(domain)
        # 从包含cname的hosts列表中提取ip和域名
    print(cname_domain_List)
    multithreaded_processor(cname_bypass, cname_domain_List)
    # 多线程处理绕过包含cname的域名

    if bypass_hosts_List is not None:
        try:
            with open('C:\\Windows\\System32\\drivers\\etc\\hosts', 'w') as file:
                # 改写hosts文件，使用真实ip与域名绑定
                file.write('\n'.join(bypass_hosts_List))
        except:
            with open('hosts', 'w') as file:
                # 无权限写入，则改写至本地，需手动替换hosts文件
                file.write('\n'.join(bypass_hosts_List))

    for ip_domain in bypass_hosts_List:
        ip, domain = ip_domain.split(' ')
        if f"{ip} {domain}" not in hosts_List:
            hosts_List.append(f"{ip} {domain}")
            # 将改写后的hosts列表添加至总的hosts列表以便scanPorts使用
    with open('hosts.txt', 'w') as file:
        file.write('\n'.join(hosts_List))
    
    for ip_domain in hosts_List:
        ip, domain = ip_domain.split(' ')
        on_line_ip_List.append(ip)
        on_line_domain_List.append(domain)
        # 提取存活的hosts列表中的ip和域名
    with open('onlineIPs.txt', 'w') as file:
        file.write('\n'.join(on_line_ip_List))
    with open('onlineDomains.txt', 'w') as file:
        file.write('\n'.join(on_line_domain_List))

    print(f"on line ips:{len(hosts_List)}")
    print(f"off line ips:{len(off_line_List)}")
    print(f"cname domains:{len(cname_hosts_List)}")
    print(f"bypass cname数量:{len(bypass_hosts_List)}")
    print("任务执行完成")
