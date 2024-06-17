
'''
文件读写服务模块
提供读取和写入文本文件的功能，用于处理域名列表等数据的存取。
'''

class ReadWriteService:
    def __init__(self, file_path):
        """初始化读写服务。
        :param file_path: 文件路径，用于指定读取和写入的文件。
        """
        self.file_path = file_path
    
    def read_txt(self):
        """读取文本文件内容。
        :return: 返回文件中每行的列表，排除空行。
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return [line.strip() for line in file if line.strip()]
        except Exception as e:
            print(f'读取文件错误: {e}')
            return []
    
    def write_txt(self, lines):
        """将列表中的数据写入文本文件。
        :param lines: 字符串列表，每个元素代表一行写入的内容。
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                file.write('\n'.join(lines))
            return True
        except Exception as e:
            print(f'写入文件错误: {e}')
            return False
