import re
import datetime
import threading
from queue import Queue
from pathlib import Path
from collections import defaultdict
from user_agents import parse


# 分析日志
def log_analysis(log_line: str):
    func_dict = {'datetime': lambda time: datetime.datetime.strptime(time, '%d/%b/%Y:%H:%M:%S %z'),  # 转换时间的对应函数
                 'request': lambda mode: dict(zip(('method', 'url', 'protocol'), mode.split())),  # 请求分解的对应函数
                 'useragent': lambda x: parse(x)
                 }

    # 用正则分组名有：remote, datetime, request, status, useragent
    # 日志格式：10.211.55.2 - - [14/Jul/2020:18:54:58 +0800] "GET / HTTP/1.1" 403 4897 "-" "curl/7.64.1"
    pattern = '''(?P<remote>^[\d.]{7,}) - - \[(?P<datetime>[^\[\]]+)\] "(?P<request>[^"]+)" (?P<status>\d{3,}) \d{3,} "[^"]+" "(?P<useragent>[^"]+)"$'''
    matcher = re.match(pattern, log_line)

    if matcher:  # 判断是否匹配上了，如未匹配，函数默认会返回 None
        return {k: func_dict.get(k, lambda x: x)(v) for k, v in
                matcher.groupdict().items()}  # matcher.groupdict() 会返回一个带分组名的字典，例如 {'remote': xxxxxxxx}


# 加载日志文件
def open_file(file):
    with open(file, encoding='utf8') as f:
        for line in f:
            d = log_analysis(line)
            if d:
                yield d
            else:
                # TODO 不合格的数据有多少
                # print('########################')
                continue


# 批量读取文件，并判断是否是文件
def load(*path):
    for file in path:
        f = Path(file)
        if not f.exists():  # 判断文件是否存在
            continue
        elif f.is_dir():  # 如果是目录，就迭代目录内的所有文件
            for x in f.iterdir():
                if x.is_file():  # 如果是文件就读取，否则就忽略了
                    yield from open_file(x)
        elif f.is_file():  # 如果是文件，就直接读取
            yield from open_file(f)


# 时间滑动窗口
def windows(src: Queue, handler, interval: int, width: int):
    """
    :param src: 数据源
    :param handler: 负责处理数据的函数
    :param interval: 时间间隔
    :param width: 时间宽度
    """
    start = datetime.datetime.strptime('1970/01/01 00:00:00 +0800', '%Y/%m/%d %H:%M:%S %z')
    current = datetime.datetime.strptime('1970/01/01 00:00:01 +0800', '%Y/%m/%d %H:%M:%S %z')
    delta = datetime.timedelta(seconds=(width - interval))  # 重复的部分 = 宽度 - 间隔

    buffer = []

    while True:
        data_dict = src.get()
        if data_dict:
            buffer.append(data_dict)
            current = data_dict['datetime']

        if (current - start).total_seconds() >= interval:
            ret = handler(buffer)

            buffer = [x for x in buffer if x['datetime'] > current - delta]
            start = current


# 消息分发器
def dispatcher(src):
    # 队列列表
    queues = []
    threads = []

    def reg(handler, interval, width):
        q = Queue()
        queues.append(q)

        t = threading.Thread(target=windows, args=(q, handler, interval, width))
        threads.append(t)

    def run():
        for t in threads:
            t.start()

        for x in src:
            for q in queues:
                q.put(x)

    return reg, run


# 状态码分析的 handler
def handler_status(buffer):
    d = {}
    start = buffer[0]['datetime']  # 因为日志是按时间顺序记录的，那么在同一个 buffer 内，第一条日志的时间就是这个 buffer 的起始时间
    end = buffer[-1]['datetime']  # 最后一条日志的时间就是这个 buffer 的结束时间

    for i in buffer:
        status = i['status']
        if status not in d.keys():
            d[status] = 0
        d[status] += 1

    # 总数
    total = sum(d.values())

    for k, v in d.items():
        p = (v / total) * 100  # 计算平均值
        d[k] = [d[k], p]  # 把平均值塞回d中

    # 输出到控制台
    print(f'在 {start.date()}【 {start.time()} - {end.time()} 】内')
    for status in d.items():
        print(' ' * 40, f'{status[0]} 出现 {status[1][0]} 次，占比 {int(status[1][1])}%')
    print('\n')

    return start, end, d


# 统计用户的浏览器
ua_dict = defaultdict(int)  # 这是记录 agent 出现次数的字典，对于 agent 的版本，看一小段时间是没有意义的，应该放在函数外，可记录下完整的次数


def user_agent(buffer):
    for i in buffer:
        ua = i['useragent']
        ua_dict[(ua.browser.family, ua.browser.version_string)] += 1

    # 输出到控制台
    print(f'截止：{buffer[-1]["datetime"]}')
    sort_ua = sorted(ua_dict.items(), key=lambda x: x[1], reverse=True)  # 按出现次数排序
    for agent in sort_ua:
        print(' ' * 40, f'客户端：{agent[0][0]:<20} 版本：{agent[0][1]:<15} 出现次数：{agent[1]}')
    print('\n')

    return ua_dict


if __name__ == '__main__':
    # 从命令行参数获取路径的方式
    # import sys
    # path = sys.argv[1]

    # 直接指定路径，测试时使用
    path = './test_file/access_1.log'

    reg, run = dispatcher(load(path))

    # 注册 handler，时间(s)：时间窗口的间隔、宽度
    # 日志会以一个时间窗口为单位，分发到注册的 handler
    # 日志已经被格式化完毕，handler 只要按自己的需求提取并选择如何处理即可
    reg(handler_status, 5, 5)  # 负责统计状态码
    reg(user_agent, 5, 5)  # 负责统计 agent 信息

    # 启动
    run()
