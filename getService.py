'''
Created on 2024. 6. 1
@author: 0x4D
get service
'''
class get:
    def __init__(self, target):
        self.target = str(target)
        self.data = self.get_ip()
    def get_ip(self):
        import re
        target = self.target
        # 提取ip地址函数
        try:
            ip_address = re.search(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}', str(target))
            # 提取ip地址
            return ip_address.group() if ip_address else None
            # 返回ip地址
        except Exception as e:
            #print(e)
            return None
            # 返回None
if __name__ == '__main__':
    target = 'asdnfiasd 192.168.1.1123ggiasd'
    print(get(target).data)
