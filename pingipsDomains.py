'''
ping ip 或 域名, 返回在线ip
'''
import re
import time
import subprocess
import concurrent.futures
from tqdm import tqdm

def pingipDomain(ipDomain):
    #ping并返回结果
    response = subprocess.run(['ping', '-n', '2', ipDomain], stdout = subprocess.PIPE, text = True, shell = True)
    #如果你是linux用户,请使用-c
    #response = subprocess.run(['ping', '-c', '2', ipDomain], stdout = subprocess.PIPE, text = True, shell = True)
    if 'ms' in str(response):
        if 'cname' in str(response):
            if ipDomain not in cnameipsdomainsList:
                cnameipsdomainsList.append(ipDomain)
        else:
            ipAddress = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', str(response))
            ipAddress = ipAddress.group()
            if ipAddress not in ipsaddressList:
                ipsaddressList.append(ipAddress)
            if ipDomain not in onlineipsdomainsList:
                onlineipsdomainsList.append(ipDomain)
            with open('log.txt', 'a') as file:
                file.write(f"{ipDomain}:{ipAddress}\n")
                if ipAddress != ipDomain:
                    if ipDomain not in urlsList:
                        urlsList.append(f"http://{ipDomain}:80")
                        urlsList.append(f"https://{ipDomain}:443")
    else:
        if ipDomain not in offlineipsdomainsList:
            offlineipsdomainsList.append(ipDomain)

if __name__ == "__main__":
    #读取文件
    fileName = 'ipsDomains.txt'
    with open(fileName, 'r') as file:
        ipsdomainsList = list(set(line.strip() for line in file if line.strip()))
    #创建时间
    timesTamp = str(int(time.time()))
    print(timesTamp)
    print(" | 主线任务进度 |")
    cnameipsdomainsList, onlineipsdomainsList, offlineipsdomainsList, ipsaddressList, urlsList = [], [], [], [], []
    with open('urlPorts.txt', 'w') as file:
        pass
    with open('log.txt', 'w') as file:
        pass
    # 创建线程池
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 批量提交任务给线程池
        for result in tqdm(executor.map(pingipDomain, ipsdomainsList), total=len(ipsdomainsList)):
            pass
        with open('onlineipsDomains.txt', 'w') as file:
            file.writelines(f"{ip}\n" for ip in onlineipsdomainsList)
        with open('onlineips.txt', 'w') as file:
            file.writelines(f"{ip}\n" for ip in ipsaddressList)
        with open('cnameipsDomains.txt', 'w') as file:
            file.writelines(f"{ip}\n" for ip in cnameipsdomainsList)
        with open('offlineipsDomains.txt', 'w') as file:
            file.writelines(f"{ip}\n" for ip in offlineipsdomainsList)
        with open('urlPorts.txt', 'w') as file:
            file.writelines(f"{url}\n" for url in urlsList)
        print("任务执行完成")
