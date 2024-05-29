'''
扫描端口, 返回可能存在的url链接。
'''
import socket
import time
import concurrent.futures
from tqdm import tqdm
import queue

#openportsList = []

def scanPorts(ip):
        
    portList = [i for i in range(1,65536)]
    openportsQueue = queue.Queue()
    
    def sanner(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)
        try:
            r = s.connect_ex((ip, port))
            if r == 0:#判断是否开启
                #openportsList.append(f"{ip}:{port}")
                openportsQueue.put(f"{ip}:{port}")# 将结果放入队列
        except:
            pass
        finally:
            s.close()
            
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 批量提交任务给线程池
        futures = [executor.submit(sanner, port) for port in portList]
        concurrent.futures.wait(futures)# 等待所有任务完成
        
    # 从队列中获取所有结果
    openportsList = [openportsQueue.get() for _ in range(openportsQueue.qsize())]
    return openportsList
    
def writeReport(ipPort):
    
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

    ip, port = ipPort.split(":")
    if port in portsFiles:
        fileName = portsFiles[port]
        with open(fileName, 'a') as file:
            file.write(f"{ip}:{port}\n")
    else:        
        with open('urlPorts.txt', 'a') as file:
            file.write(f"http://{ipPort}\nhttps://{ipPort}\n")

def clearingGarbages(openportsList, threshold):
    ipCounts = {}
    for ipPort in openportsList:
        ip, _ = ipPort.split(":")  # 只获取IP部分
        ipCounts[ip] = ipCounts.get(ip, 0) + 1

    # 过滤掉IP出现次数大于阈值的项
    newopenportsList = list(set([ipPort for ipPort in openportsList if ipCounts[ipPort.split(":")[0]] <= threshold]))
    garbagesList = list(set([ipPort for ipPort in openportsList if ipCounts[ipPort.split(":")[0]] >= threshold]))
    with open("garbages.txt", 'w') as file:
        file.writelines(f"{ipPort}\n" for ipPort in garbagesList)
    return newopenportsList

if __name__ == "__main__":
    #读取文件
    fileName = 'onlineips.txt'
    with open(fileName, 'r') as file:
        ipsList = list(set(line.strip() for line in file if line.strip()))
    #创建时间
    timesTamp = str(int(time.time()))
    print(timesTamp)
    print(" | 第 1 任务进度 |")
    # 创建线程池
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 批量提交任务给线程池
        openportsList = list(tqdm(executor.map(scanPorts, ipsList), total = len(ipsList)))
    #清楚垃圾
    newopenportsList = clearingGarbages(openportsList, 100)
    print(" | 第 2 任务进度 |")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 批量提交任务给线程池
        for result in tqdm(executor.map(writeReport, newopenportsList), total = len(newopenportsList)):
            pass
            
    print("任务执行完成")
