'''
访问url链接, 返回可以访问的url并做成书签,方便burpsuite一键开启,以及返回一张方便nmap和goby等扫描工具扫描的txt文件
'''
import re
import time
import requests
from multiprocessServiceOptimized import MultiProcessService
from readwriteServiceOptimized import ReadWriteService
from accesscheckServiceOptimized import AccessCheckService

class BookMarkService:
    def __init__(self, write_method='a', book_mark_path='bookMark.html', nmap_scan_payh='nmapScan.txt'):
        self.book_mark_path = book_mark_path
        self.nmap_scan_payh = nmap_scan_payh
        self.write_method = write_method
        self.new_ips_domains_list = []
        self.body_list = []
    def domain_check(self, target):
        """发送 HTTP或HTTPS 请求。
        :param target: 要请求的域名。
        :return: 提取到的网站页面信息。
        """
        result = AccessCheckService(target)
        return result.maker_urls()
    def write_book_mark(self, data_list=list(ReadWriteService("bookMark.txt").read_txt())):
        def write_body(url):
            if url is not None:
                body = f'	<DT><A HREF="{url}" ADD_DATE={Datetime}">{url}</A>\n'
                if body not in self.body_list:
                    self.body_list.append(body)
        Datetime = str(int(time.time()))
        head = [f'<!DOCTYPE NETSCAPE-Bookmark-file-1>\n<!-- This is an automatically generated file.\n     It will be read and overwritten.\n     DO NOT EDIT! -->\n<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n<TITLE>Bookmarks</TITLE>\n<H1>Bookmarks</H1>\n<DL><p>\n    <DT><H3 ADD_DATE="2716597092" LAST_MODIFIED="0" PERSONAL_TOOLBAR_FOLDER="true">BOOK</H3>\n    <DL><p>\n    </DL><p>\n']
        ReadWriteService(self.book_mark_path).write_txt(head)
        print(" | 主线任务进度 |")
        urls_list = MultiProcessService(self.domain_check, data_list).execute()
        MultiProcessService(write_body, urls_list).execute()
        ReadWriteService(self.book_mark_path, self.write_method).write_txt(self.body_list)
        dlp = ['</DL><p>\n']
        ReadWriteService(self.book_mark_path, self.write_method).write_txt(dlp)
        print(" | 主线任务完成 |")

if __name__ == "__main__":
    BookMarkService().write_book_mark()

