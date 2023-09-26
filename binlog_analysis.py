import re
import sys
import argparse
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
    WriteRowsEvent,
    UpdateRowsEvent,
    DeleteRowsEvent
)

# 设置命令行参数
parser = argparse.ArgumentParser(description='Binlog Analysis Tool')

parser.add_argument('-H', '--host', metavar='<host>', type=str, required=True,
                    help='the MySQL server host (default: 127.0.0.1)')
parser.add_argument('-P', '--port', metavar='<port>', type=int, default=3306,
                    help='the MySQL server port (default: 3306)')
parser.add_argument('-u', '--user', metavar='<user>', type=str, required=True,
                    help='the MySQL user name')
parser.add_argument('-p', '--password', metavar='<password>', type=str, required=True,
                    help='the MySQL password')
parser.add_argument('-d', '--database', metavar='<database>', type=str, required=True,
                    help='the database schema name')
parser.add_argument('-c', '--charset', metavar='<charset>', type=str, default='utf8',
                    help='the MySQL connection character set (default: utf8)')
parser.add_argument('-s', '--start', metavar='<start_index>', type=str, required=True,
                    help='the start index of binlog files, e.g. mysql-bin.000001')
parser.add_argument('-e', '--end', metavar='<end_index>', type=str,
                    help='the end index of binlog files, e.g. mysql-bin.000003')
                    
args = parser.parse_args()

# 定义MySQL连接设置
source_mysql_settings = {
    "host": args.host,
    "port": args.port,
    "user": args.user,
    "passwd": args.password,
    "database": args.database,
    "charset": args.charset
}

# 解析起始和结束索引
start_index = int(args.start.split('.')[-1])
end_index = int(args.end.split('.')[-1]) if args.end else start_index

# 根据开始和结束索引生成文件名列表
log_files = []
for i in range(start_index, end_index+1):
    # 将文件名拼接起来
    file_name = args.start.split('.')[0] + f'.{i:06d}'
    log_files.append(file_name)

print(f'process binlog files is : {log_files}\n')

# 定义记录表的字典
table_counts = {}

# 定义Binlog解析器
for log_file in log_files:
    # 提取文件名中的数字部分
    file_number = int(re.search(r'\d+', log_file).group())
    
    stream = BinLogStreamReader(connection_settings=source_mysql_settings, 
                                server_id=123456789,
                                log_file=log_file, 
                                resume_stream=False)

    # 开始读取日志
    for binlogevent in stream:
        # 只处理数据行事件
        if isinstance(binlogevent, (WriteRowsEvent, UpdateRowsEvent, DeleteRowsEvent)):
            # 获取事件的表名和操作类型
            table = binlogevent.table
            event_type = type(binlogevent).__name__
        
            # 初始化记录表的计数器
            if table not in table_counts:
                table_counts[table] = {'insert': 0, 'update': 0, 'delete': 0}
        
            # 根据操作类型更新计数器
            if event_type == 'WriteRowsEvent':
                table_counts[table]['insert'] += 1
            elif event_type == 'UpdateRowsEvent':
                table_counts[table]['update'] += 1
            elif event_type == 'DeleteRowsEvent':
                table_counts[table]['delete'] += 1


# 按照操作次数排序输出最终结果
sorted_table_counts = sorted(table_counts.items(), 
                             key=lambda x: sum(x[1].values()), reverse=True)

# 打印当前文件的统计结果
for table, counts in sorted_table_counts:
    print(f'{table}: {counts}\n')
