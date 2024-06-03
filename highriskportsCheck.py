import paramiko
import time
import queue
import concurrent.futures
from tqdm import tqdm
from ftplib import FTP

def check21Login(hostName):

    with open('21userNames.txt', 'r') as file:
        usernamesList = list(set(line.strip() for line in file if line.strip()))
    with open('21passWords.txt', 'r') as file:
        passwordsList = list(set(line.strip() for line in file if line.strip()))
    
    def attack(userName):
        
        try:
            ftp = FTP(hostName)
            ftp.login(userName, passWord)
            #print("登录成功")
            with open ('loginSuccess.txt', 'a') as file:
                file.write(f'{hostName}:21 usr:{userName} pwd:{passWord}\n')
            ftp.quit()
            return True
        except Exception as e:
            #print(f"登录失败: {e}")
            return False
        
    for passWord in passwordsList:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 批量提交任务给线程池
            for result in executor.map(attack, usernamesList):
                pass


def check22Login(hostName):

    with open('22userNames.txt', 'r') as file:
        usernamesList = list(set(line.strip() for line in file if line.strip()))
    with open('22passWords.txt', 'r') as file:
        passwordsList = list(set(line.strip() for line in file if line.strip()))
    
    def attack(userName):
        
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostName, 22, userName, passWord)
            stdin, stdout, stderr = ssh.exec_command('ls')
            #print(stdout.read().decode())
            ssh.close()
            with open ('loginSuccess.txt', 'a') as file:
                file.write(f'{hostName}:22 usr:{userName} pwd:{passWord}\n')
            return True
        except paramiko.AuthenticationException:
            #print("Authentication failed, please verify your credentials.")
            return False
        except paramiko.SSHException as e:
            #print(f"SSH connection failed: {e}")
            return False
        except Exception as e:
            #print(f"Other error occurred: {e}")
            return False
        
    for password in passwordsList:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 批量提交任务给线程池
            for result in executor.map(attack, usernamesList):
                pass
 

if __name__ == "__main__":

    checksList = {}
        
    portsFiles = {
        "21":{"checkFunction": check21Login, "ipsList": []},
        "22":{"checkFunction": check22Login, "ipsList": []},
        #"1521":{"checkFunction": check1521Login, "ipsList": []},
        #"3306":{"checkFunction": check3306Login, "ipsList": []},
        #"6379":{"checkFunction": check6379Login, "ipsList": []},
        #"7001":{"checkFunction": check7001Login, "ipsList": []},
        }

     # 读取文件
    try:
        with open('highriskPorts.txt', 'r') as file:
            for line in file:
                ipPort = line.strip().split(":")
                if len(ipPort) == 2:
                    ip, port = ipPort
                    if port in portsFiles:
                        portInfo = portsFiles[port]
                        portInfo["ipsList"].append(ip)
    except Exception as e:
        print(f"读取文件失败: {e}")
    
    # 并发执行登录检查
    print(f"弱口令用户检测开始，请等待")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {}
        tasks = sum(len(portInfo["ipsList"]) for port, portInfo in portsFiles.items())  # 计算总任务数
        with tqdm(total = tasks) as tqdmTask:
            for port, portInfo in portsFiles.items():
                checkFunction = portInfo["checkFunction"]
                ipsList = portInfo["ipsList"]
                for ip in ipsList:
                    hostName = f"{ip}:{port}"
                    future = executor.submit(checkFunction, hostName)
                    futures[future] = hostName
            
            # 打印检查结果
            for future in concurrent.futures.as_completed(futures):
                hostName = futures[future]
                try:
                    result = future.result()
                    if result:
                        #print(f"{hostName} 登录成功")
                        pass
                    else:
                        tqdm
                        #print(f"{hostName} 登录失败")
                        pass
                except Exception as e:
                    print(f"检查 {hostName} 时发生错误: {e}")
                tqdmTask.update()
        print("检查完成")
