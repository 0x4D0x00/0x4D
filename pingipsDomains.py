'''
ping ip 或 域名, 返回在线ip
'''
import subprocess
import concurrent.futures
import time
import re
global threads
threadsList = []

def pingipDomain(ipDomain):
    #ping并返回结果
    response = subprocess.run(['ping', '-n', '2', ipDomain], stdout=subprocess.PIPE, text=True, shell=True)
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
    print("创建任务")
    cnameipsdomainsList, onlineipsdomainsList, offlineipsdomainsList, ipsaddressList = [], [], [], []
    # 创建线程池
    threads = 1
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 批量提交任务给线程池
        for result in executor.map(pingipDomain, ipsdomainsList):
            threads += 1
            print("任务: No." +str(threads)+" 执行完成...请等待")
        print("总执行任务数量: "+str(threads))
        with open('onlineipsDomains.txt', 'w') as file:
            file.writelines(f"{ip}\n" for ip in onlineipsdomainsList)
        print("在线ipsDomains已写入完成")
        with open('onlineips.txt', 'w') as file:
            file.writelines(f"{ip}\n" for ip in ipsaddressList)
        print("在线ips已写入完成")
        with open('cnameipsDomains.txt', 'w') as file:
            file.writelines(f"{ip}\n" for ip in cnameipsdomainsList)
        with open('offlineipsDomains.txt', 'w') as file:
            file.writelines(f"{ip}\n" for ip in offlineipsdomainsList)
        print("任务执行完成")
