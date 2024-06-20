'''
访问检测服务
''' 
from multiprocessServiceOptimized import MultiProcessService
class AccessCheckService:
    def __init__(self, target):
        self.target = target
    def access_service(self):
        '''
        使用url访问检测
        '''
        import requests
        try:
            response = requests.get(self.target, timeout = 5)
            content = response.text
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
        
# 示例用法
if __name__ == "__main__":
    
    domain_list = ["www.baidu.com", "www.google.com", "www.bing.com"]
    def domain_check(target):
        result = AccessCheckService(target)
        return result.check_access()
    result = MultiProcessService(domain_check, domain_list).execute()
    print(result)
    
    url_list = ["http://www.baidu.com", "http://www.google.com", "http://www.bing.com"]
    def url_check(target):
        result = AccessCheckService(target)
        return result.access_service()
    result = MultiProcessService(url_check, url_list).execute()
    print(result)
