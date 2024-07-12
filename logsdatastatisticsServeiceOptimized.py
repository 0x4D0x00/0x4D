from readwriteServiceOptimized import ReadWriteService
from multiprocessServiceOptimized import MultiProcessService
from collections import OrderedDict
class LogsDataStatisticsServeice(ReadWriteService, MultiProcessService):
    def __init__(self):
        """
        #   加载服务
        """
        super().__init__()
    def min_and_max(self):
        '''
        #   取字典中最大和最小的键
        '''
        min_key = min(list(self.temporary_data_statistics.keys()))
        max_key = max(list(self.temporary_data_statistics.keys()))
        return min_key, max_key
    def max_value_func(self):
        '''
        #   取字典中最大值的键和值函数
        '''
        max_key = max(self.temporary_data_statistics, key = self.temporary_data_statistics.get)
        max_value = self.temporary_data_statistics[max_key]
        return max_key, max_value
    def comprehensive_data_statistics_func(self, data_str):
        '''
        #   统计指定参数次数的函数
        '''
        if str(data_str) not in self.temporary_data_statistics:
            self.temporary_data_statistics[data_str] = 0
        data_times = self.temporary_data_statistics.get(data_str, 0)
        self.temporary_data_statistics[data_str] = data_times + 1
    def most_attack_ip_data_statistics(self, time_period):
        '''
        #   统计最具攻击性IP, 以及攻击次数
        '''
        self.Thread_execute_no_tqdm(self.comprehensive_data_statistics_func, self.title_names_dict['攻击ip'])
        most_attack_ip, most_attack_times = self.max_value_func()
        index = self.title_names_dict['攻击ip'].index(most_attack_ip)
        attack_address = self.title_names_dict['源归属地'][index]
        self.comprehensive_data_statistics.append(f"\n重点关注对象\n{time_period} 最具攻击性IP: {most_attack_ip}, 归属地: {attack_address}, 攻击: {most_attack_times} 次")
        self.temporary_data_statistics = {}
        return most_attack_ip
    def data_statistics(self, time_period):
        '''
        #   通用型数据统计函数
        '''
        '''
        #   统计攻击类型, 以及各攻击次数
        '''
        self.Thread_execute_no_tqdm(self.comprehensive_data_statistics_func, self.title_names_dict['分组类型'])
        for attack_type, attack_times in self.temporary_data_statistics.items():
            self.comprehensive_data_statistics.append(f"{time_period} {attack_type} {attack_times} 次")
        self.temporary_data_statistics = {}
        '''
        #   统计各威胁等级, 以及各威胁等级数量
        '''
        self.Thread_execute_no_tqdm(self.comprehensive_data_statistics_func, self.title_names_dict['威胁等级'])
        for threat_level, attack_times in self.temporary_data_statistics.items():
            self.comprehensive_data_statistics.append(f"{time_period} {threat_level} {attack_times} 次")
        self.temporary_data_statistics = {}
        '''
        #   统计被攻击次数最多的目标IP, 以及被攻击次数
        '''
        self.Thread_execute_no_tqdm(self.comprehensive_data_statistics_func, self.title_names_dict['被攻击IP'])
        most_target_ip, attacked_times = self.max_value_func()
        self.comprehensive_data_statistics.append(f"{time_period} 被频繁发起攻击的目标IP: {most_target_ip}, 被攻击: {attacked_times} 次")
        self.temporary_data_statistics = {}
        '''
        #   统计主要被攻击端口, 以及被攻击次数
        '''
        self.Thread_execute_no_tqdm(self.comprehensive_data_statistics_func, self.title_names_dict['目的端口'])
        most_target_port, attacked_times = self.max_value_func()
        self.comprehensive_data_statistics.append(f"{time_period} 被频繁发起攻击的目标IP端口: {most_target_port}, 被攻击: {attacked_times} 次")
        self.temporary_data_statistics = {}
        '''
        #   统计主要攻击类型, 以及攻击次数
        '''
        self.Thread_execute_no_tqdm(self.comprehensive_data_statistics_func, self.title_names_dict['分组类型'])
        attack_type, attack_times = self.max_value_func()
        self.comprehensive_data_statistics.append(f"{time_period} 被频繁发起攻击的攻击类型主要为: {attack_type}, 攻击: {attack_times} 次")
        self.temporary_data_statistics = {}

    def unit_logs_list(self, info_str):
        '''
        #   以单位进行分类, 填充属于各单位的数据.
        '''
        if str(self.unit) in info_str:
            self.unit_names_dict[self.unit].append(str(info_str))
        
    def col_data_statistics(self, info_str):
        '''
        #   以标题进行分类, 填充属于各标题的数据
        '''
        data_list = [data_value.strip() for data_value in info_str.split(' 20% ') if data_value.strip()]
        for key, value in zip(self.title_names_dict.keys(), data_list):
            self.title_names_dict[key].append(value)
    def statistics_main(self, logs_path, rules_path="saasRules.xls", report_path="被攻击数据统计.txt"):
        '''
        #   日志读取, 日志数据分类, 日志数据统计主函数
        '''
        self.logs_path = logs_path
        self.rules_path = rules_path
        full_time_period = f"全部时段"
        peak_time_period = f"峰值时段"
        print(f"读取文件中...请稍后...")
        '''
        #   读取日志告警excel文件
        '''
        saas_logs_list = self.read_excel(self.logs_path)
        '''
        #   提取标题
        '''
        saas_titles = saas_logs_list[0]
        del saas_logs_list[0]
        '''
        #   标题命名列表
        '''
        self.title_names_dict = OrderedDict((title_name, []) for title_name in saas_titles.split(' 20% '))
        '''
        #   单位名称命名列表
        '''
        self.unit_names_dict = OrderedDict((unit_name, []) for unit_name in [info_str.split(' 20% ')[6] for info_str in saas_logs_list])
        print(f"日志数据分类")
        for unit in self.unit_names_dict.keys():
            '''
            #   日志导入以单位名称进行分类的列表
            '''
            self.unit = unit
            self.Thread_execute_no_tqdm(self.unit_logs_list, saas_logs_list)
        '''
        #   以单位为任务单元
        '''
        for unit, logs in self.unit_names_dict.items():
            '''
            #   初始化标题分类列表
            '''
            self.title_names_dict = OrderedDict((title_name, []) for title_name in self.title_names_dict)
            '''
            #   多线程日志导入以标题名称进行分类
            '''
            self.Thread_execute_no_tqdm(self.col_data_statistics, logs)
            print(f"{unit} 日志数据统计中...请稍后...")
            most_attack_ip_logs = []#      最具攻击性IP列表
            apex_attack_time_logs = []#    峰值时段日志列表
            self.comprehensive_data_statistics = []
            self.temporary_data_statistics = {}
            '''
            #   统计日志时间范围
            '''
            attack_time_list = [attack_time.split(' ')[0] for attack_time in self.title_names_dict['攻击时间']]#  攻击时间列表
            self.Thread_execute_no_tqdm(self.comprehensive_data_statistics_func, attack_time_list)
            start_date, end_date = self.min_and_max()
            self.comprehensive_data_statistics.append(f"日志统计时间范围: {start_date} 至 {end_date}")
            self.temporary_data_statistics = {}
            '''
            #   统计单位被攻击总数
            '''
            self.comprehensive_data_statistics.append(f"单位: {unit}, 总计被攻击: {len(self.title_names_dict['攻击ip'])} 次")
            '''
            #   调取通用日志统计函数
            '''
            self.data_statistics(full_time_period)
            '''
            #   缩小统计范围,锁定最具攻击性IP产生的日志
            '''
            most_attack_ip = self.most_attack_ip_data_statistics(full_time_period)
            for info_str in logs:
                if most_attack_ip in info_str:
                    most_attack_ip_logs.append(info_str)
            self.title_names_dict = OrderedDict((title_name, []) for title_name in self.title_names_dict)
            self.Thread_execute_no_tqdm(self.col_data_statistics, most_attack_ip_logs)
            self.data_statistics(full_time_period)
            most_attack_ip_logs = []
            '''
            #   统计攻击峰值时段,并重复以上步骤.
            '''
            self.Thread_execute(self.comprehensive_data_statistics_func, attack_time_list)
            apex_attack_time, apex_attack_time_attacked_times = self.max_value_func()
            self.comprehensive_data_statistics.append(f"\n攻击的峰值出现在 {apex_attack_time}, 共被攻击: {apex_attack_time_attacked_times} 次")
            self.temporary_data_statistics = {}
            for info_str in logs:
                if apex_attack_time in info_str:
                    apex_attack_time_logs.append(info_str)
            self.title_names_dict = OrderedDict((title_name, []) for title_name in self.title_names_dict)
            self.Thread_execute_no_tqdm(self.col_data_statistics, apex_attack_time_logs)
            self.data_statistics(peak_time_period)
            most_attack_ip_logs = []
            most_attack_ip = self.most_attack_ip_data_statistics(peak_time_period)
            for info_str in apex_attack_time_logs:
                if most_attack_ip in info_str:
                    most_attack_ip_logs.append(info_str)
            self.title_names_dict = OrderedDict((title_name, []) for title_name in self.title_names_dict)
            self.Thread_execute_no_tqdm(self.col_data_statistics, most_attack_ip_logs)
            self.data_statistics(peak_time_period)
            most_attack_ip_logs = []
            '''
            #   输出报告
            '''
            self.write_file(f"{unit}{report_path}", lines=self.comprehensive_data_statistics)
        print(f"数据统计完成")

if __name__ == '__main__':
    logs_path = '正面攻击告警日志20240712165359.xls'
    ops = LogsDataStatisticsServeice()
    ops.statistics_main(logs_path)
