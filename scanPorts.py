import socket
import time
import concurrent.futures
openportList = []

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
    print("创建线程")
    # 创建线程池
    threads = 1
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 批量提交任务给线程池
        for result in executor.map(scanPorts, ipsList):
            threads += 1
            print("任务: No." +str(threads)+" 执行完成...请等待")
        with open('scanPorts.txt', 'w') as file:
            file.writelines(f"http://{ipPort}\nhttps://{ipPort}\n" for ipPort in openportList)
        print("端口扫描已完成")
