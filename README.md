# binlog_analysis
Binlog分析工具-binlog_analysis.py

```shell> pip3 install mysql-replication -i "http://mirrors.aliyun.com/pypi/simple" --trusted-host "mirrors.aliyun.com"```

## 用途：高峰期排查哪些表TPS比较高

#### Usage: python3 binlog_analysis.py <start_index> [<end_index>]

```shell> python3 binlog_analysis.py mysql-bin.049622 mysql-bin.049628```

或

```shell> python3 binlog_analysis.py mysql-bin.049622```

输出结果：
```new_qrtz_schedule_job: {'insert': 0, 'update': 82652, 'delete': 0}

withdraw_close_send: {'insert': 185, 'update': 456, 'delete': 0}

api_channel_check_record: {'insert': 306, 'update': 0, 'delete': 0}

user_contract: {'insert': 140, 'update': 140, 'delete': 0}

user_limit_change_log: {'insert': 96, 'update': 96, 'delete': 0}

user_limit_record_log: {'insert': 187, 'update': 0, 'delete': 0}

user_coupon_task: {'insert': 0, 'update': 123, 'delete': 0}```
