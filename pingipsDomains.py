'''
ping ip 或 域名, 返回在线ip
'''
import subprocess
import concurrent.futures

def pingipDomain(ipDomain):
    #ping并返回结果
    response = subprocess.run(['ping', '-n', '2', ipDomain], stdout=subprocess.PIPE, text=True, shell=True)
    if 'ms' in str(response):
        if 'cname' in str(response):
            cnameipsDomainsList.append(ipDomain)
        else:
            onlineipsDomainsList.append(ipDomain)       
    else:
        offlineipsDomainsList.append(ipDomain)

if __name__ == "__main__":
    #读取文件
    fileName = 'ipsDomains.txt'
    with open(fileName, 'r') as file:
        ipsDomainsList = list(set(line.strip() for line in file if line.strip()))
        
    print("创建任务")
    cnameipsDomainsList, onlineipsDomainsList, offlineipsDomainsList = [], [], []
    # 创建线程池
    threads = 0
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 批量提交任务给线程池
        for result in executor.map(pingipDomain, ipsDomainsList):
            threads += 1
            print("任务: No." +str(threads)+" 执行完成")
        print("总执行任务数量: "+str(threads))
        with open('onlineipsDomains.txt', 'a') as file:
            file.writelines(f"{ip}\n" for ip in onlineipsDomainsList)
        print("在线ip已写入完成")
        with open('cnameipsDomains.txt', 'a') as file:
            file.writelines(f"{ip}\n" for ip in cnameipsDomainsList)
        with open('offlineipsDomains.txt', 'a') as file:
            file.writelines(f"{ip}\n" for ip in offlineipsDomainsList)
        print("任务完成")
