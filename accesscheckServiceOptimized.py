'''
访问检测服务
''' 
class AccessCheckService:
    def __init__(self, target):
        self.target = target
        self.user_agent = "User-Agent: Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0"
        self.cookies = ""
    def access_service(self):
        '''
        使用url访问检测
        '''
        import requests
        
        try:
            response = requests.get(self.target, headers=self.user_agent, timeout = 5)
            content = response.text
            self.cookies = response.cookies
            if response.status_code == 200 and "Not Found" not in content and "errcode" not in content and "Forbidden" not in content and "Unauthorized" not in content and "Bad Request" not in content:
                return f"{content}"
            else:
                return None
        except:
            return None
    def check_access(self):
        '''
        将域名生成url访问检测
        '''
        self.target = f"http://{self.target}"
        content  = self.access_service()
        if content is None:
            self.target = f"https://{self.target}"
            content  = self.access_service()
            if content is None:
                return "None"
            else:
                return content
        else:
            return content
    def maker_urls(self):
        self.target = f"http://{self.target}"
        content  = self.access_service()
        if content is None:
            self.target = f"https://{self.target}"
            content  = self.access_service()
            if content is None:
                pass
            else:
                return f"https://{self.target}"
        else:
            return f"http://{self.target}"

# 示例用法
if __name__ == "__main__":
    from multiprocessServiceOptimized import MultiProcessService
    domain_list = ["www.baidu.com", "www.google.com", "www.bing.com"]
    def domain_check(target):
        """发送 HTTP或HTTPS 请求。
        :param target: 要请求的域名。
        :return: 提取到的网站页面信息。
        """
        result = AccessCheckService(target)
        return result.check_access()
    result = MultiProcessService(domain_check, domain_list).execute()
    print(result)
    
    url_list = ["http://www.baidu.com", "http://www.google.com", "http://www.bing.com"]
    def url_check(target):
        """发送 HTTP或HTTPS 请求。
        :param target: 要请求的URL链接。
        :return: 提取到的网站页面信息。
        """
        result = AccessCheckService(target)
        return result.access_service()
    result = MultiProcessService(url_check, url_list).execute()
    print(result)
