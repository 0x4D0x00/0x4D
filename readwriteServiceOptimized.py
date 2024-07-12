
'''
文件读写服务模块
提供读取和写入文本文件的功能，用于处理域名列表等数据的存取。
'''
import pandas
from tqdm import tqdm
class ReadWriteService:
    def __init__(self):
        """初始化读写服务。
        :param file_path: 文件路径，用于指定读取和写入的文件。
        """
        pass
    
    def read_file(self, file_path=None, read_method='r', encoding='utf-8'):
        """读取文本文件内容。
        :return: 返回文件中每行的列表，排除空行。
        """
        try:
            with open(file_path, read_method, encoding=encoding) as file:
                return file.read()
        except Exception as e:
            print(f'读取文件错误: {e}')
            return None
    def read_file_to_list(self, file_path=None, read_method='r', encoding='utf-8'):
        """读取文本文件内容。
        :return: 返回文件中每行的列表，排除空行。
        """
        try:
            with open(file_path, read_method, encoding=encoding) as file:
                return [line.strip() for line in tqdm(file, desc="Reading file", unit="lines") if line.strip()]
        except Exception as e:
            print(f'读取文件错误: {e}')
            return []
    
    def write_file(self, file_path=None, write_method='w', encoding='utf-8', lines=None):
        """将列表中的数据写入文本文件。
        :param lines: 字符串列表，每个元素代表一行写入的内容。
        """
        try:
            with open(file_path, write_method, encoding=encoding) as file:
                file.write('\n'.join(lines))
            return True
        except Exception as e:
            try:
                with open(file_path, write_method, encoding=encoding) as file:
                    for line in tqdm(lines, desc="Writing lines", unit="lines"):
                        file.write(f"{line}" + '\n')
                return True
            except:
                print(f'写入文件错误: {e}')
                return False

    def read_excel(self, file_path=None, sheet_name=0, header=None, start_row=0, start_col=None):
        try:
            read_data = pandas.read_excel(file_path, sheet_name, header=header, skiprows=start_row, usecols=start_col)
            result_list = []
            for index, row in  tqdm(read_data.iterrows(), desc="Reading excel", unit="rows"):
                if start_row is not None and index < start_row:
                    continue
                row_data = ' 20% '.join(map(str, row.fillna('null').tolist()))
                result_list.append(row_data)
            return result_list
        except Exception as e:
            print(f'读取Excel文件错误: {e}')
            return []

if __name__ == '__main__':
    mylist = ["1","2","3"]
    ReadWriteService().write_file(file_path="test.txt", lines=mylist)
