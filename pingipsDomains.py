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
                    if f"{ipDomain}:{ipAddress}" not in logsList:
                        logsList.append(f"{ipDomain}:{ipAddress}")
        else:
            if f"{ipDomain}" not in offlineipsdomainsList:
                offlineipsdomainsList.append(f"{ipDomain}")
    except:
        pass
    
if __name__ == "__main__":
    
    #读取文件
    fileName = 'ipsDomains.txt'
    with open(fileName, 'r') as file:
        ipsdomainsList = list(set(line.strip() for line in file if line.strip()))
    #创建时间
    timesTamp = str(int(time.time()))
    print(timesTamp)
    print(" | 主线任务进度 |")
    cnameipsdomainsList, onlineipsdomainsList, offlineipsdomainsList, ipsaddressList, domainsList, logsList = [], [], [], [], [], []
    # 创建线程池
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 批量提交任务给线程池
        for result in tqdm(executor.map(pingipDomain, ipsdomainsList), total=len(ipsdomainsList)):
            pass
        #写入报告
        with open('logs.txt', 'w') as file:
            file.write('\n'.join(logsList))
        with open('onlineIPs.txt', 'w') as file:
            file.writelines(f"{ip}\n" for ip in ipsaddressList)
        with open('onlineDomains.txt', 'w') as file:
            file.writelines(f"{domain}\n" for domain in domainsList)
        '''以下内容备用
        #with open('onlineipsDomains.txt', 'w') as file:
            #file.writelines(f"{ipDomain}\n" for ipDomain in onlineipsdomainsList)
        #with open('cnameServers.txt', 'w') as file:
            #file.writelines(f"{ipDomain}\n" for ipDomain in cnameipsdomainsList)
        #with open('offlineServers.txt', 'w') as file:
            #file.writelines(f"{ipDomain}\n" for ipDomain in offlineipsdomainsList)
        '''
        print("任务执行完成")
