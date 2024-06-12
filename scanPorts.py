'''
扫描端口, 返回可能存在的url链接。
'''
import socket
import time
import concurrent.futures
from tqdm import tqdm
import queue

def scanPorts(ip):

    #####################################################
    #定义扫描端口数量（暂时65535个，改变数字可自定义范围）
    portList = [i for i in range(1,65535)]
    #####################################################
    
    openportsQueue = queue.Queue()
    
    def sanner(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)
        try:
            r = s.connect_ex((ip, port))
            if r == 0:# 判断是否开启
                openportsQueue.put(f"{ip}:{port}")# 将结果放入队列
        except:
            pass
        finally:
            s.close()
            
    with concurrent.futures.ThreadPoolExecutor() as executor:# 批量提交任务给线程池
        futures = [executor.submit(sanner, port) for port in portList]
        concurrent.futures.wait(futures)# 等待所有任务完成
        
    openportsList = [openportsQueue.get() for _ in range(openportsQueue.qsize())]# 从队列中获取所有结果
    return openportsList
    
def writeReport(ipsPorts):
    
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
    
    ip, port = ipsPorts.split(":")
    ip = str(ip)
    port = str(port)
    if port in portsFiles:
        fileName = portsFiles[port]# 暂时不使用fileName
        highriskPortsList.append(f"{ip}:{port}")
    else:
        if ipsPorts not in urlsList:
            urlsList.append(f"http://{ipsPorts}")
            urlsList.append(f"https://{ipsPorts}")

def clearingGarbages(openportsList, threshold):
    ipCounts = {}
    for ipPort in openportsList:
        ip, _ = ipPort.split(":")# 只获取IP部分
        ipCounts[ip] = ipCounts.get(ip, 0) + 1

    newopenportsList = list(set([ipPort for ipPort in openportsList if ipCounts[ipPort.split(":")[0]] <= threshold]))# 过滤掉IP出现次数大于阈值的对象

    garbagesList = list(set([ipPort for ipPort in openportsList if ipCounts[ipPort.split(":")[0]] >= threshold]))# 记录垃圾内容

    for ipPort in garbagesList:
        ip, _ = ipPort.split(":")
        if ip not in temporaryList:
            temporaryList.append(ip)
    
    with open("garbages.txt", 'w') as file:
        file.writelines("\n".join(garbagesList))
    
    return newopenportsList

if __name__ == "__main__":
    
    try:# 读取文件
        with open('onlineIPs.txt', 'r') as file:
            ripsList = list(set(line.strip() for line in file if line.strip()))
        with open('onlineDomains.txt', 'r') as file:
            rdomainsList = list(set(line.strip() for line in file if line.strip()))
        with open('hosts.txt', 'r') as file:
            hosts_List = list(set(line.strip() for line in file if line.strip()))
    except:
        pass

    with open('highriskPorts.txt', 'w') as file:# 刷新
        pass
    
    temporaryList, urlsList, highriskPortsList = [], [], []# 创建列表

    timesTamp = str(int(time.time()))# 创建时间
    print(timesTamp)
    
    print(" | 主线任务进度 |")# 创建线程池
    with concurrent.futures.ThreadPoolExecutor() as executor:# 批量提交任务给线程池
        resultList = list(tqdm(executor.map(scanPorts, ripsList), total = len(ripsList)))
    openportsList = [ipPort for ipsPorts in resultList for ipPort in ipsPorts]# 合并所有IP的开放端口列表（如果需要）
    
    ###############################################################
    # 清除垃圾（阈值设置100：超过100个端口的ip将被记录在垃圾数据中）
    newopenportsList = clearingGarbages(openportsList, 100)
    ###############################################################
    
    print(" | 支线任务进度 |")
    with concurrent.futures.ThreadPoolExecutor() as executor:# 批量提交任务给线程池
        for result in tqdm(executor.map(writeReport, newopenportsList), total = len(newopenportsList)):
            pass
      
    ipDomainMap = {ip: domain for ip, domain in (entry.split(' ') for entry in hosts_List)}# 创建字典，存储映射  

    for ip in temporaryList:# 过滤temporaryList中的IP，找出它们对应的域名，并从rdomainsList中删除这些域名
        if ip in ipDomainMap:
            domain = ipDomainMap[ip]
            if domain in rdomainsList:
                rdomainsList.remove(domain)
    for domain in rdomainsList:
        if domain not in urlsList:
            urlsList.append(f"http://{domain}")
            urlsList.append(f"https://{domain}")
    
    with open('urlsList.txt', 'w') as file:# 输出内容
        file.writelines("\n".join(urlsList))
    with open('highriskPorts.txt', 'w') as file:
        file.write("\n".join(highriskPortsList))
    print("任务执行完成")
