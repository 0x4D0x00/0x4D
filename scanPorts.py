'''
扫描端口, 返回可能存在的url链接。
'''
import socket
import time
import concurrent.futures
from tqdm import tqdm

def scanPorts(ip):
        
    portList = [i for i in range(1,65536)]
    
    def sanner(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)
        r = s.connect_ex((ip, port))
        if r == 0:#判断是否开启
            openportList.append(f"{ip}:{port}")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 批量提交任务给线程池
        for result in executor.map(sanner, portList):
            pass

if __name__ == "__main__":
    #读取文件
    fileName = 'onlineips.txt'
    with open(fileName, 'r') as file:
        ipsList = list(set(line.strip() for line in file if line.strip()))
    #创建时间
    timesTamp = str(int(time.time()))
    print(timesTamp)
    print(" | 主线任务进度 |")
    openportList = []
    # 创建线程池
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 批量提交任务给线程池
        for result in tqdm(executor.map(scanPorts, ipsList), total = len(ipsList)):
            pass
        with open('scanPorts.txt', 'a') as file:
            file.writelines(f"http://{ipPort}\nhttps://{ipPort}\n" for ipPort in openportList)
        print("任务执行完成")
