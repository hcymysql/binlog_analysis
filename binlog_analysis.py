import sys
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
    WriteRowsEvent,
    UpdateRowsEvent,
    DeleteRowsEvent
)


# 连接MySQL数据库
source_mysql_settings = {
    "host": "192.168.188.197",
    "port": 3307,
    "user": "admin",
    "passwd": "123456",
    "database": "test",
    "charset": "utf8"
}

# 定义记录表的字典
table_counts = {}

# 获取命令行参数
log_files = sys.argv[1:]

# 指定Binlog文件并定义Binlog解析器
for log_file in log_files:
    stream = BinLogStreamReader(connection_settings=source_mysql_settings, 
                                server_id=197307,
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

# 按照操作次数排序输出结果
sorted_table_counts = sorted(table_counts.items(), 
                             key=lambda x: sum(x[1].values()), reverse=True)
for table, counts in sorted_table_counts:
    print(f'{table}: {counts}')
