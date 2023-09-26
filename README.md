# binlog_analysis
Binlog分析工具-binlog_analysis

```shell> chmod 755 binlog_analysis```

## 用途：高峰期排查哪些表TPS比较高

#### Usage: ./binlog_analysis <start_index> [<end_index>]

```shell> ./binlog_analysis -H 192.168.188.197 -u admin -p '123456' -d test -s mysql-bin.049622 -e mysql-bin.049628```

或

```shell> ./binlog_analysis -H 192.168.188.197 -u admin -p '123456' -d test -s mysql-bin.049622```

输出结果：
```new_qrtz_schedule_job: {'insert': 0, 'update': 82652, 'delete': 0}

withdraw_close_send: {'insert': 185, 'update': 456, 'delete': 0}

api_channel_check_record: {'insert': 306, 'update': 0, 'delete': 0}

user_contract: {'insert': 140, 'update': 140, 'delete': 0}

user_limit_change_log: {'insert': 96, 'update': 96, 'delete': 0}

user_limit_record_log: {'insert': 187, 'update': 0, 'delete': 0}

user_coupon_task: {'insert': 0, 'update': 123, 'delete': 0}```
