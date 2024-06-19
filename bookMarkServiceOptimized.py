'''
访问url链接, 返回可以访问的url并做成书签,方便burpsuite一键开启,以及返回一张方便nmap和goby等扫描工具扫描的txt文件
'''
import re
import time
import requests
from multiprocessServiceOptimized import MultiProcessService
from readwriteServiceOptimized import ReadWriteService

class BookMarkService:
    def __init__(self, data_path="urlsList.txt", write_method='a', book_mark_path='bookMark.html', nmap_scan_payh='nmapScan.txt'):
        self.data_path = data_path
        self.book_mark_path = book_mark_path
        self.nmap_scan_payh = nmap_scan_payh
        self.write_method = write_method
        self.iis7_list = []
        self.nginx_list = []
        self.other_list = []
        self.new_ips_domains_list = []
        self.body_list = []
    
    def scanner(self, url):
    
        try:
            response = requests.get(url, timeout = 5)
            content = response.text
            statusCode = response.status_code
            if statusCode == 200:
                if "IIS7" in content:
                    if f"{url}" not in self.iis7_list:
                        self.iis7_list.append(f"{url}")
                elif "Welcome to nginx!" in content:
                    if f"{url}" not in self.nginx_list:
                        self.nginx_list.append(f"{url}")
                elif "限制" not in content and "无法正常工作" not in content and "认证失败" not in content and "window.wx" not in content and "请稍后再试" not in content and "防火墙" not in content and "云防御" not in content and "errcode" not in content and "Not Found" not in content:
                    if f"{url}" not in self.other_list:
                        self.other_list.append(f"{url}")
                        pattern = r"(https?://)|(:\d{1,5})"
                        newipDomain = re.sub(pattern, "", url)
                        if f"{newipDomain}" not in self.new_ips_domains_list:
                            self.new_ips_domains_list.append(f"{newipDomain}")
        except:
            pass

    def write_book_mark(self):
        def write_body(url):
            body = f'	<DT><A HREF="{url}" ADD_DATE={Datetime}">{url}</A>\n'
            if body not in self.body_list:
                self.body_list.append(body)
        Datetime = str(int(time.time()))
        head = [f'<!DOCTYPE NETSCAPE-Bookmark-file-1>\n<!-- This is an automatically generated file.\n     It will be read and overwritten.\n     DO NOT EDIT! -->\n<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n<TITLE>Bookmarks</TITLE>\n<H1>Bookmarks</H1>\n<DL><p>\n    <DT><H3 ADD_DATE="2716597092" LAST_MODIFIED="0" PERSONAL_TOOLBAR_FOLDER="true">BOOK</H3>\n    <DL><p>\n    </DL><p>\n']
        ReadWriteService(self.book_mark_path).write_txt(head)
        urlsList = ReadWriteService(self.data_path).read_txt()
        print(" | 主线任务进度 |")
        MultiProcessService(self.scanner, urlsList).execute()
        MultiProcessService(write_body, self.other_list).execute()
        ReadWriteService(self.book_mark_path, self.write_method).write_txt(self.body_list)
        dlp = ['</DL><p>\n']
        ReadWriteService(self.book_mark_path, self.write_method).write_txt(dlp)
        ReadWriteService(self.nmap_scan_payh).write_txt(self.new_ips_domains_list)
        print(" | 主线任务完成 |")

if __name__ == "__main__":
    BookMarkService().write_book_mark()

