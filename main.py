'''
Created on 2024. 6. 1
@author: 0x4D
Who am i ? So i can be who i want to be!
This is main file
'''
def ping_ip_domain(ip_domain):
    from pingService import ping
    return ping(ip_domain).data
#print(ping_info)
def get_ip(information_str):
    from getService import get
    #x = get(information_str).data[:-4]
    return get(information_str).data
def retrieval_ips_domains(ip_domain):
    # 检索ip地址和域名函数
    result = ping_ip_domain(f"{ip_domain}")
    # 发送ping命令获取ping的报文信息
    if result:
        ip_address = get_ip(f"{result}")
        # 提取ip地址
        if ip_address is not None:
            if 'cname' in f"{result}":
                # 判断是否存在cname
                if f"{ip_address} {ip_domain}" not in cname_hosts_List:
                    cname_hosts_List.append(f"{ip_address} {ip_domain}")
            else: 
                if ip_address:
                    hosts_List.append(f"{ip_address} {ip_domain}")
                    # 不包含cname地址则加入hosts列表中
    return cname_hosts_List, hosts_List
    # 返回hosts列表和包含cname的hosts列表
def cname_bypass(cname_info):
    # cname bypass 第一次尝试函数
    import re
    ip_address, domain = cname_info.split(' ')
    try:
        retrieval_domain_Name = re.search(r'\b[^.]+\.(gov|org|cn|com|net|edu|mil|int)+.*$\b', str(domain))
        # 尝试将多级域名缩减为二级域名，并保留顶级域名（顶级域名不全，用到时加入即可）
        # 例如：www.baidu.com 缩减为 baidu.com
        new_domain = retrieval_domain_Name.group()
        if new_domain != domain:
            #print(new_domain)
            #bypass_retrieval(f"{domain}", f"{new_domain}")
            ping_info = ping_ip_domain(f"{new_domain}")
            new_ip = get_ip(f"{ping_info}")
            if new_ip is not None:
                if f"{new_ip} {domain} {new_domain}" not in bypass_retrieval_List:
                    bypass_retrieval_List.append(f"{new_ip} {domain} {new_domain}")
            # 尝试绕过二级域名
        else:
            #print(f'{domain} 进行域名重组')
            #domain_creat(f"{domain}")
            #multiProcess(domain_creat, domain_name_List).data
            # 如果上面尝试失败，则该域名本身就为二级域名，尝试拼接为三级域名。
            # 获取原始域名的ip地址
            if f"{ip_address} {domain}" not in domain_creat_List:
                domain_creat_List.append(f"{ip_address} {domain}")
    except Exception as e:
        if f"{ip_address} {domain}" not in domain_creat_List:
            domain_creat_List.append(f"{ip_address} {domain}")
        print(e)
def domain_creat(information_str):
    # 尝试重构域名函数
    if information_str is not None:
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
def bypass_retrieval(information_str):
    # 检索cname bypass成败函数
    if information_str is not None:
        ip, domain, new_domain = information_str.split(' ')
    #print(information_str)
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
            if cname_ip != new_ip:
                # 判断新域名和原始域名ip地址是否为同一网段
                if f"{new_ip} {domain}" not in bypass_hosts_List:
                    bypass_hosts_List.append(f"{new_ip} {domain}")
                    # 将新ip和原始域名地址写入该hosts列表
    except Exception as e:
        pass
        #print(e)
def scan_ports(host):
    import socket
    ip, domain = host.split(' ')
    #####################################################
    #定义扫描端口数量（暂时65535个，改变数字可自定义范围）
    portList = [i for i in range(1,65536)]
    #####################################################
    def scanner(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)
        try:
            r = s.connect_ex((ip, port))
            if r == 0:# 判断是否开启
                open_ports_List.append(f"{ip}:{port}")# 将开启的端口写入该列表
        except:
            pass
        finally:
            s.close()
    multiProcess(scanner, portList).data
def clearingGarbages(open_ports_List, threshold):
    ipCounts = {}
    for ip_port in open_ports_List:
        ip, _ = ip_port.split(":")# 只获取IP部分
        ipCounts[ip] = ipCounts.get(ip, 0) + 1

    new_open_ports_List = list(set([ip_port for ip_port in open_ports_List if ipCounts[ip_port.split(":")[0]] <= threshold]))
    # 过滤掉IP出现次数大于阈值的对象
    garbages_List = list(set([ip_port for ip_port in open_ports_List if ipCounts[ip_port.split(":")[0]] >= threshold]))
    # 记录垃圾内容
    for ip_port in garbages_List:
        ip, _ = ip_port.split(":")
        if ip not in temporary_List:
            temporary_List.append(ip)
    readWrite("c:\\Program Files (x86)\\Tools\\jobTools\\garbages.txt").write_txt(garbages_List)
    return new_open_ports_List
def write_report(ip_ports):
    
    portsFiles = {
        "21":"21ftpPorts.txt",
        "22":"22sshPorts.txt",
        "23":"23telnetPorts.txt",
        "25":"25smtpPorts.txt",
        "53":"53dnsPorts.txt",
        "69":"69tftpPorts.txt",
        "110":"110pop3Ports.txt",
        "135":"135rpcPorts.txt",
        "139":"smbPorts.txt",
        "445":"smbPorts.txt",
        "5985":"smbPorts.txt",
        "143":"143imapPorts.txt",
        "389":"389ldapPorts.txt",
        "1521":"1521oraclePorts.txt",
        "3306":"3306mysqlPorts.txt",
        "3389":"3389rdpPorts.txt",
        "5432":"5432postgresqlPorts.txt",
        "6379":"6379redisPorts.txt",
        "7001":"7001weblogicPorts.txt",
        "9000":"9000fcgiPorts.txt",
        "9200":"9200elastcsearchPorts.txt"
        }
    
    ip, port = ip_ports.split(":")
    ip = str(ip)
    port = str(port)
    if port in portsFiles:
        fileName = portsFiles[port]# 暂时不使用fileName
        highrisk_ports_List.append(f"{ip}:{port}")
    else:
        if ip_ports not in urls_List:
            urls_List.append(f"http://{ip_ports}")
            urls_List.append(f"https://{ip_ports}")
def wait_for_input_or_timeout(prompt, timeout):
    import threading
    # 创建一个事件对象，用于在超时后通知主线程
    event = threading.Event()
    # 创建一个守护线程来等待输入
    def input_thread():
        try:
            user_input = input(prompt)
            # 如果有输入，设置事件
            event.set()
        except EOFError:
            pass  # 处理Ctrl+D（在Unix/Linux上）或Ctrl+Z（在Windows上）
    
    # 启动守护线程
    input_thread_obj = threading.Thread(target=input_thread, daemon=True)
    input_thread_obj.start()
    
    # 等待事件或超时
    if event.wait(timeout):
        return input_thread_obj.user_input
    else:
        return None  # 超时返回None
if __name__ == '__main__':
    print("read config file")
    import time
    from readwriteService import readWrite
    from multiprocessService import multiProcess
    cname_hosts_List = []
    hosts_List = []
    bypass_retrieval_List = []
    domain_creat_List = []
    bypass_hosts_List = []
    ips_domains_List = readWrite("c:\\Program Files (x86)\\Tools\\jobTools\\ipsDomains.txt").read_txt()
    domain_name_List = readWrite("c:\\Program Files (x86)\\Tools\\jobTools\\domainnamesDict.txt").read_txt()
    print("ping ips and domains")
    multiProcess(retrieval_ips_domains, ips_domains_List).data
    print("bypass cname domains")
    # 输入是否要扫描端口
    prompt = "press any key to continue...(y/n) or wait 5 seconds: "
    timeout = 5  # 秒
    result = wait_for_input_or_timeout(prompt, timeout)
    if result is not None:
        pass
    else:
        multiProcess(cname_bypass, cname_hosts_List).data
        print("creat domain")
        multiProcess(domain_creat, domain_creat_List).data
        print("bypass retrieval domains")
        multiProcess(bypass_retrieval, bypass_retrieval_List).data
        if bypass_hosts_List is not None:
            readWrite("C:\\Windows\\System32\\drivers\\etc\\hosts").write_txt(bypass_hosts_List)
    readWrite("c:\\Program Files (x86)\\Tools\\jobTools\\highriskPorts.txt").write_txt()
    print("scan ports")
    # 输入是否要扫描端口
    prompt = "press any key to continue...(y/n) or wait 5 seconds: "
    timeout = 5  # 秒
    result = wait_for_input_or_timeout(prompt, timeout)
    if result is not None:
        pass
    else:
        temporary_List = []
        urls_List = []
        highriskports_List = []
        open_ports_List = []
        temporary_List = []
        highrisk_ports_List = []
        urls_List = []
        r_domains_List = []
        multiProcess(scan_ports, hosts_List).data
        ###############################################################
        # 清除垃圾（阈值设置100：超过100个端口的ip将被记录在垃圾数据中）
        new_open_ports_List = clearingGarbages(open_ports_List, 100)
        ###############################################################
        multiProcess(write_report, new_open_ports_List).data
        ipDomainMap = {ip: domain for ip, domain in (entry.split(' ') for entry in hosts_List)}# 创建字典，存储映射
        for ip in temporary_List:# 过滤temporaryList中的IP，找出它们对应的域名，并从r_domains_List中删除这些域名
            if ip in ipDomainMap:
                domain = ipDomainMap[ip]
                if domain in r_domains_List:
                    r_domains_List.remove(domain)
        for domain in r_domains_List:
            if domain not in urls_List:
                urls_List.append(f"http://{domain}")
                urls_List.append(f"https://{domain}")
        readWrite("c:\\Program Files (x86)\\Tools\\jobTools\\highriskPorts.txt").write_txt(highrisk_ports_List)
        readWrite("c:\\Program Files (x86)\\Tools\\jobTools\\urls.txt").write_txt(urls_List)
