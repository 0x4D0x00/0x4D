'''
ping ip 或 域名, 返回在线ip
'''
import re
import time
import subprocess
import dns.resolver
import concurrent.futures
from tqdm import tqdm

def searchgithubdnsServers(ipDomain):
    
    try:
        resolver = dns.resolver.Resolver()
        answers = resolver.resolve(ipDomain, 'dns')
        for ipAddress in answers:
            dnsserversList.append(f"{ipAddress.address}")
            if ipAddress is not None:
                cnameipsdomainsList.remove(ipDomain)
                domainsbundledIpsList.append(f"{ipDomain}:{ipAddress.address}")
                ipsaddressList.append(f"{ipAddress.address}")
                onlineipsdomainsList.append(f"{ipDomain}")
        return dnsserversList
    except Exception as e:
        pass
def pingipDomain(ipDomain):
    
    try:
        response = subprocess.run(['ping', '-n', '2', ipDomain], stdout = subprocess.PIPE, text = True, shell = True)   # ping并返回结果,如果你是Linux用户,请将-n改为-c
        if 'ms' in str(response):   # 寻找存活目标
            if 'cname' in str(response):    # 筛查附带云防御目标
                if f"{ipDomain}" not in cnameipsdomainsList:
                    cnameipsdomainsList.append(f"{ipDomain}")
            else:
                ipAddress = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', str(response))   # 提取ip地址
                ipAddress = ipAddress.group()
                if f"{ipAddress}" not in ipsaddressList:
                    ipsaddressList.append(f"{ipAddress}")
                if f"{ipDomain}" not in onlineipsdomainsList:
                    onlineipsdomainsList.append(f"{ipDomain}")
                if ipAddress != ipDomain and f"{ipDomain}" not in domainsList:
                    domainsList.append(f"{ipDomain}")
                    if f"{ipDomain}:{ipAddress}" not in domainsbundledIpsList:
                        domainsbundledIpsList.append(f"{ipDomain}:{ipAddress}")
        else:
            if f"{ipDomain}" not in offlineipsdomainsList:
                offlineipsdomainsList.append(f"{ipDomain}")
    except:
        pass
def cnameBypass(domain):

    def domainCreat(domain):
        for domainName in domainnamesList:
            newdomain = f"{domainName}" + "." + f"{domain}"
            if f"{newdomain}" not in newDomainsList:
                newDomainsList.append(f"{newdomain}")
                bypassList.append(f"{newdomain}:{domain}")
        return newDomainsList, bypassList
    try:
        ipAddress = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', str(domain))
        if ipAddress:
            newdomain = ipAddress.group()
            if newdomain:
                pass
        else:
            retrievaldomainName = re.search(r'\.[^.]+\.[^.]+$', str(domain))
            if retrievaldomainName:
                newdomain = retrievaldomainName.group()[1:]
                if newdomain:
                    if f"{newdomain}" not in newDomainsList:
                        newDomainsList.append(f"{newdomain}")
                        bypassList.append(f"{newdomain}:{domain}")
            else:
                domainCreat(domain)
    except Exception as e:
        print(f"{e}")
    
if __name__ == "__main__":
    
    fileName = 'ipsDomains.txt' # 读取文件
    try:
        with open(fileName, 'r') as file:
            ipsdomainsList = list(set(line.strip() for line in file if line.strip()))
    except:
        with open(fileName, 'w') as file:
            pass
        print('ipsDomains.txt文件内容为空。')
    timesTamp = str(int(time.time()))   # 创建时间
    print(timesTamp)
    print(" | ping ip/域名 |")
    cnameipsdomainsList, onlineipsdomainsList, offlineipsdomainsList, ipsaddressList, domainsList, domainsbundledIpsList, newDomainsList, bypassList, hostsList, dnsserversList = [], [], [], [], [], [], [], [], [], []    # 创建列表
    with concurrent.futures.ThreadPoolExecutor() as executor:   # 第1次ping
        for result in tqdm(executor.map(pingipDomain, ipsdomainsList), total=len(ipsdomainsList)):  # 批量提交任务给线程池
            pass
    print(" | 查询dns记录 |")
    with concurrent.futures.ThreadPoolExecutor() as executor:   # 查看cname域名历史dns记录
        for result in tqdm(executor.map(searchgithubdnsServers, cnameipsdomainsList), total=len(cnameipsdomainsList)): # 批量提交任务给线程池
            pass
    
    with concurrent.futures.ThreadPoolExecutor() as executor:   # 第2次ping
        for result in tqdm(executor.map(pingipDomain, dnsserversList), total=len(dnsserversList)): # 批量提交任务给线程池
            pass
    try:
        with open("domainnamesDict.txt", 'r') as file:  # 读取域名字典
            domainnamesList = list(set(line.strip() for line in file if line.strip()))
    except:
        domainnamesList = []
        print('domainnamesDict.txt文件内容为空。')
    print(" | 域名bypass |")
    with concurrent.futures.ThreadPoolExecutor() as executor:   # cname域名bypass尝试
        for result in tqdm(executor.map(cnameBypass, cnameipsdomainsList), total=len(cnameipsdomainsList)): # 批量提交任务给线程池
            pass
    with open('oldcnameServers.txt', 'w') as file:
        file.writelines('\n'.join(cnameipsdomainsList))
    with open('domainsbundledIps.txt', 'w') as file:    #写入报告
        file.write('\n'.join(domainsbundledIpsList))
    cnameipsdomainsList = []    # 重置记录
    domainsbundledIpsList = []
    print(" | 总结归纳 |")
    with concurrent.futures.ThreadPoolExecutor() as executor:   # 第3次ping
        for result in tqdm(executor.map(pingipDomain, newDomainsList), total=len(newDomainsList)):  # 批量提交任务给线程池
            pass
    for bundledItem in domainsbundledIpsList:
        domain, ip = bundledItem.split(':')
        for bypassItem in bypassList:
            bypassDomain, targetDomain = bypassItem.split(':')
            if domain == bypassDomain: # 如果找到相同的第一个值，则组合为'ip targetDomain'并添加到hostsList中
                if f"{ip} {targetDomain}" not in hostsList:
                    hostsList.append(f'{ip} {targetDomain}')
    #class后转为调用其他函数
    with open('domainsbundledIps.txt', 'a') as file:    #写入报告
        file.write('\n'.join(domainsbundledIpsList))
    with open('onlineIPs.txt', 'w') as file:
        file.write('\n'.join(ipsaddressList))
    with open('onlineDomains.txt', 'w') as file:
        file.write('\n'.join(domainsList))
    with open('newcnameServers.txt', 'w') as file:
        file.write('\n'.join(cnameipsdomainsList))
    try:
        with open('C:\\Windows\\System32\\drivers\\etc\\hosts', 'a') as file:   # 改写hosts文件，使用真实ip与域名绑定
            file.write('\n'.join(hostsList))
    except:
        with open('hosts', 'w') as file:
            file.write('\n'.join(hostsList))
    '''以下内容备用
    with open('onlineipsDomains.txt', 'w') as file:
        file.writelines(f"{ipDomain}\n" for ipDomain in onlineipsdomainsList)
    with open('offlineServers.txt', 'w') as file:
        file.writelines(f"{ipDomain}\n" for ipDomain in offlineipsdomainsList)
    '''
    print("任务执行完成")
