'''
Created on 2024. 6. 1
@author: 0x4D
read and write service
'''
class readWrite:
    def __init__(self, target):
        self.target = f"{target}"
        self.iterable = []
    def read_txt(self):
        target = self.target
        try:
            with open(target, 'r') as file:
                iterable = list(set(line.strip() for line in file if line.strip()))
            return iterable
        except:
            print('File not found')
            return []
    def write_txt(self, iterable):
        target = self.target
        try:
            with open(target, 'w') as file:
                file.write('\n'.join(iterable))
            return True
        except:
            for line in iterable:
                print(f"{line}")
                return f"{line}"
if __name__ == '__main__':
    file_name = 'ipsDomains.txt'
    read_List = readWrite(file_name).read_txt()
    print(read_List)
    
    file_name = 'text.txt'
    write_List = ['192.168.1.1', '192.168.1.2']
    write_file = readWrite(file_name).write_txt(write_List)
