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
            cnameipsdomainsList.append(ipDomain)
        else:
            ipAddress = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', str(response))
            ipAddress = ipAddress.group()
            ipsaddressList.append(ipAddress) 
            onlineipsdomainsList.append(ipDomain)
            with open('log.txt', 'a') as file:
                file.writelines(f"{ipDomain}:{ipAddress}\n" for ip in ipsaddressList)
    else:
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
    cnameipsdomainsList, onlineipsdomainsList, offlineipsdomainsList, ipsaddressList = [], [], [], []
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
        print("任务执行完成")
