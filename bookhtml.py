'''
访问url链接, 返回可以访问的url并做成书签，方便burpsuite一键开启，以及返回一张方便nmap和goby等扫描工具扫描的txt文件
'''
import re
import time
import requests
import concurrent.futures
from tqdm import tqdm

def rsc(url):
    
    try:
        response = requests.get(url, timeout = 5)
        content = response.text
        statusCode = response.status_code
        #print(statusCode)
        if statusCode == 200:
            if "IIS7" in content:
                if f"{url}" not in iis7List:
                    iis7List.append(f"{url}")
            elif "Welcome to nginx!" in content:
                if f"{url}" not in nginxList:
                    nginxList.append(f"{url}")
            elif "限制" not in content and "无法正常工作" not in content and "认证失败" not in content and "window.wx" not in content and "请稍后再试" not in content:
                if f"{url}" not in otherList:
                    otherList.append(f"{url}")
                    pattern = r"(https?://)|(:\d{1,5})"
                    newipDomain = re.sub(pattern, "", url)
                    if f"{newipDomain}" not in newipsdomainsList:
                        newipsdomainsList.append(f"{newipDomain}")
    except:
        pass

if __name__ == "__main__":
    #刷新
    iis7List, nginxList, otherList, newipsdomainsList = [], [], [], []
    Datetime = str(int(time.time()))
    #创建书签
    with open('书签.html', 'w') as htmlFile:
        st = f'<!DOCTYPE NETSCAPE-Bookmark-file-1>\n<!-- This is an automatically generated file.\n     It will be read and overwritten.\n     DO NOT EDIT! -->\n<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n<TITLE>Bookmarks</TITLE>\n<H1>Bookmarks</H1>\n<DL><p>\n    <DT><H3 ADD_DATE="2716597092" LAST_MODIFIED="0" PERSONAL_TOOLBAR_FOLDER="true">BOOK</H3>\n    <DL><p>\n    </DL><p>\n'
        htmlFile.writelines(st)
    #获取url
    with open('urlsList.txt', 'r') as scanFile:
        urlsList = list(set([url.strip() for url in scanFile if url.strip()]))
    #获取可访问页面
    print(" | 主线任务进度 |")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for result in tqdm(executor.map(rsc, urlsList), total=len(urlsList)):
            pass
    with open('书签.html', 'a') as file:
        file.writelines(f'	<DT><A HREF="{url}" ADD_DATE={Datetime}">{url}</A>\n' for url in otherList)
    with open('nginxPorts.txt', 'w') as file:
        file.writelines("\n".join(nginxList))
    with open('IIS7Ports.txt', 'w') as file:
        file.writelines("\n".join(iis7List))
    with open('nmapScan.txt', 'w') as file:
        file.writelines("\n".join(newipsdomainsList))
    #书签完成
    with open('书签.html', 'a') as htmlFile:
        dlp = '</DL><p>\n'
        htmlFile.write(dlp)
    print('任务执行完成')
