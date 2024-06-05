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
        #ping并返回结果,如果你是Linux用户,请将-n改为-c
        response = subprocess.run(['ping', '-n', '2', ipDomain], stdout = subprocess.PIPE, text = True, shell = True)
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
    
if __name__ == "__main__":
    
    #读取文件
    fileName = 'ipsDomains.txt'
    try:
        with open(fileName, 'r') as file:
            ipsdomainsList = list(set(line.strip() for line in file if line.strip()))
    except:
        print('没有ipsDomains.txt文件')
    #创建时间
    timesTamp = str(int(time.time()))
    print(timesTamp)
    print(" | 主线任务进度 |")
    cnameipsdomainsList, onlineipsdomainsList, offlineipsdomainsList, ipsaddressList, domainsList, domainsbundledIpsList, domainsList = [], [], [], [], [], [], []
    # 创建线程池
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 批量提交任务给线程池
        for result in tqdm(executor.map(pingipDomain, ipsdomainsList), total=len(ipsdomainsList)):
            tqdm.update()
        print(" | 支线任务进度 |")
        # 尝试 bypass cname 域名
        for domain in cnameipsdomainsList:
            retrieval = re.search(r'\.[a-zA-Z0-9]{2,}\.[a-zA-Z]{2,}', domain)
            domain = retrieval.group()[1:]
            if f"{domain}" not in domainsList:
                domainsList = append.(f"{domain}")
        # 重置列表
        cnameipsdomainsList = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
        # 批量提交任务给线程池
            for result in tqdm(executor.map(pingipDomain, domainsList), total=len(domainsList)):
                tqdm.update()
            #写入报告
            with open('domainsbundledIps.txt', 'w') as file:
                file.write('\n'.join(domainsbundledIpsList))
            with open('onlineIPs.txt', 'w') as file:
                file.writelines('\n'.join(ipsaddressList))
            with open('onlineDomains.txt', 'w') as file:
                file.writelines('\n'.join(domainsList))
            with open('cnameServers.txt', 'w') as file:
                file.writelines('\n'.join(cnameipsdomainsList))
        '''以下内容备用
        #with open('onlineipsDomains.txt', 'w') as file:
            #file.writelines(f"{ipDomain}\n" for ipDomain in onlineipsdomainsList)
        #with open('offlineServers.txt', 'w') as file:
            #file.writelines(f"{ipDomain}\n" for ipDomain in offlineipsdomainsList)
        '''
        print("任务执行完成")
