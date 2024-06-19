from readwriteServiceOptimized import ReadWriteService
from readwriteServiceOptimized import ReadWriteService
from multiprocessServiceOptimized import MultiProcessService

class LogAnalysisServeice:
    def __init__(self, logs_path, rules_path, report_path, logs_sheet=0, rules_sheet=0, report_sheet=0):
        """初始化读写服务。
        :param file_path: 文件路径，用于指定读取和写入的文件。
        """
        self.logs_path = logs_path
        self.logs_sheet = logs_sheet
        self.rules_path = rules_path
        self.rules_sheet = rules_sheet
        self.report_path = report_path
        self.report_sheet = report_sheet
    def saas_logs_analysis(self):
        '''
        日志分析,将告警日志与规则进行匹配，输出匹配结果
        '''
        print("开始读取文件")
        saas_logs_list = ReadWriteService(self.logs_path, self.logs_sheet).read_excel()
        saas_rule_list = ReadWriteService(self.rules_path, self.rules_sheet).read_excel()
        write_list = []
        def logs_analysis(rule_method):
            def write_report(info_str):
                if rule_method in info_str:
                    if info_str not in write_list:
                        write_list.append(info_str)
            rule_number, rule_id, rule_method = rule_method.split(' ')
            MultiProcessService(write_report, saas_logs_list).execute()
            return write_list
        print("开始分析")
        MultiProcessService(logs_analysis, saas_rule_list).execute()
        print("输出报告")
        ReadWriteService(self.report_path).write_txt(write_list)
if __name__ == '__main__':
    logs_path = '正面攻击告警日志20240618111523.xls'
    rules_path = 'saasRules.xls'
    report_path = 'saaslogsanalysisReport.txt'
    logs_sheet = '正面攻击告警日志0-13'
    ops = LogAnalysisServeice(logs_path, rules_path, report_path, logs_sheet)
    ops.saas_logs_analysis()
