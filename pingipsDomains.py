'''
ping ip 或 域名, 返回在线ip
'''
import re
import time
import subprocess
import concurrent.futures
from tqdm import tqdm

def pingipDomain(ipDomain):

    try:
        response = subprocess.run(['ping', '-n', '2', ipDomain], stdout = subprocess.PIPE, text = True, shell = True)   # ping并返回结果,如果你是Linux用户,请将-n改为-c
        if 'ms' in str(response):
            if 'cname' in str(response):
                if f"{ipDomain}" not in cnameipsdomainsList:
                    cnameipsdomainsList.append(f"{ipDomain}")                
            else:
                ipAddress = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', str(response))
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
                for domainName in domainnamesList:
                    newdomain = f"{domainName}" + "." + f"{domain}"
                    if f"{newdomain}" not in newDomainsList:
                        newDomainsList.append(f"{newdomain}")
                        bypassList.append(f"{newdomain}:{domain}")
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
    print(" | 主线任务进度 |")
    cnameipsdomainsList, onlineipsdomainsList, offlineipsdomainsList, ipsaddressList, domainsList, domainsbundledIpsList, newDomainsList, bypassList, hostsList = [], [], [], [], [], [], [], [], []    # 创建列表
    with concurrent.futures.ThreadPoolExecutor() as executor:   # 创建线程池
        for result in tqdm(executor.map(pingipDomain, ipsdomainsList), total=len(ipsdomainsList)):  # 批量提交任务给线程池
            pass
    print(" | 支线任务进度 |")
    try:
        with open("domainnamesDict.txt", 'r') as file:
            domainnamesList = list(set(line.strip() for line in file if line.strip()))
    except:
        print('没有domainnamesDict.txt文件')
    print(" | 域名创建进度 |")
    with concurrent.futures.ThreadPoolExecutor() as executor:   # 创建线程池
        for result in tqdm(executor.map(cnameBypass, cnameipsdomainsList), total=len(cnameipsdomainsList)): # 批量提交任务给线程池
            pass
    with open('oldcnameServers.txt', 'w') as file:
        file.writelines('\n'.join(cnameipsdomainsList))
    with open('domainsbundledIps.txt', 'w') as file:    #写入报告
        file.write('\n'.join(domainsbundledIpsList))
    cnameipsdomainsList = []    # 重置记录
    domainsbundledIpsList = []
    print(" | 域名筛查进度 |")
    with concurrent.futures.ThreadPoolExecutor() as executor:   # 创建线程池
        for result in tqdm(executor.map(pingipDomain, newDomainsList), total=len(newDomainsList)):  # 批量提交任务给线程池
            pass
    print(domainsbundledIpsList)
    print(bypassList)
    for bundledItem in domainsbundledIpsList:
        domain, ip = bundledItem.split(':')
        for bypassItem in bypassList:
            bypassDomain, targetDomain = bypassItem.split(':')
            if domain == bypass_domain: # 如果找到相同的第一个值，则组合为'ip targetDomain'并添加到hostsList中
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
        with open('C:\\Windows\\System32\\drivers\\etc\\hosts', 'a') as file:
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
