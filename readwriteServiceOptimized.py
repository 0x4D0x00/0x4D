
'''
文件读写服务模块
提供读取和写入文本文件的功能，用于处理域名列表等数据的存取。
'''

class ReadWriteService:
    def __init__(self, file_path, write_method='w', sheet_name=0, header=None, start_row=None, start_col=None):
        """初始化读写服务。
        :param file_path: 文件路径，用于指定读取和写入的文件。
        """
        self.file_path = file_path
        self.write_method = write_method
        self.sheet_name = sheet_name
        self.start_row = start_row
        self.start_col = start_col
        self.header = header
    
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
            with open(self.file_path, self.write_method, encoding='utf-8') as file:
                file.write('\n'.join(lines))
            return True
        except Exception as e:
            print(f'写入文件错误: {e}')
            return False

    def read_excel(self):
        import pandas
        try:
            read_data = pandas.read_excel(self.file_path, self.sheet_name, header=self.header, skiprows=self.start_row, usecols=self.start_col)
            result_list = []
            for index, row in read_data.iterrows():
                if self.start_row is not None and index < self.start_row:
                    continue
                row_data = ' '.join(map(str, row.dropna().tolist()))
                result_list.append(row_data)
            return result_list
        except Exception as e:
            print(f'读取Excel文件错误: {e}')
            return []
