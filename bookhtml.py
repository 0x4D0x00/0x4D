'''
访问url链接, 返回可以访问的url并做成书签，方便burpsuite一键开启
'''
import time
import requests
import concurrent.futures
from tqdm import tqdm

def rsc(url):

    Datetime = str(int(time.time()))
    
    try:
        response = requests.get(url, timeout = 5)
        statusCode = response.status_code
        #print(statusCode)
        if statusCode == 200:
            with open('书签.html', 'a') as htmlFile:
                dtA = f'	<DT><A HREF="{url}" ADD_DATE={Datetime}">{url}</A>\n'
                htmlFile.writelines(dtA)
        else:
            pass
    except:
        pass

if __name__ == "__main__":
    #创建书签
    with open('书签.html', 'w') as htmlFile:
        st = f'<!DOCTYPE NETSCAPE-Bookmark-file-1>\n<!-- This is an automatically generated file.\n     It will be read and overwritten.\n     DO NOT EDIT! -->\n<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n<TITLE>Bookmarks</TITLE>\n<H1>Bookmarks</H1>\n<DL><p>\n    <DT><H3 ADD_DATE="2716597092" LAST_MODIFIED="0" PERSONAL_TOOLBAR_FOLDER="true">BOOK</H3>\n    <DL><p>\n    </DL><p>\n'
        htmlFile.writelines(st)
    #获取url
    with open('scanPorts.txt', 'r') as scanFile:
        urlList = [url.strip() for url in scanFile]
    #获取可访问页面
    print(" | 主线任务进度 |")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for result in tqdm(executor.map(rsc, urlList), total=len(urlList)):
            pass
    #书签完成
    with open('书签.html', 'a') as htmlFile:
        dlp = '</DL><p>\n'
        htmlFile.writelines(dlp)
    print('任务执行完成')
