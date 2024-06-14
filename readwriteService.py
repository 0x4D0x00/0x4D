'''
Created on 2024. 6. 1
@author: 0x4D
read and write service
'''
class readWrite:
    def __init__(self, file_name):
        self.file_name = f"{file_name}"
        self.write_List = []
    def read_txt(self):
        file_name = self.file_name
        try:
            with open(file_name, 'r') as file:
                iterable = list(set(line.strip() for line in file if line.strip()))
            return iterable
        except:
            print('File not found')
            return []
    def write_txt(self, iterable):
        file_name = self.file_name
        try:
            with open(file_name, 'w') as file:
                file.write('\n'.join(iterable))
            return True
        except:
            for line in iterable:
                print(f"{line}")
            pass
if __name__ == '__main__':
    file_name = 'ipsDomains.txt'
    read_List = readWrite(file_name).read_txt()
    print(read_List)
    
    file_name = 'text.txt'
    write_List = ['192.168.1.1', '192.168.1.2']
    write_file = readWrite(file_name).write_txt(write_List)
