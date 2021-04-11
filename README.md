# Apache Log Analysis

Apache 日志分析框架

- 自动分析有效数据并分发；
- 采用生产者消费者解耦模型，默认使用单机 Q，可更换为 Redis 或 RabbitMQ 等；
- 支持时间窗口，支持定义宽度、间隔；
- 支持自定义插件注册；
- 自带插件：
    - 浏览器版本分析；
    - 状态码分析；

# 使用方法

日志会被自动分析，并以字典的格式分发，例如：

```python
{
    'remote': '123.125.71.36',
    'datetime': datetime.datetime(2017, 4, 6, 18, 9, 25, tzinfo=datetime.timezone(datetime.timedelta(seconds=28800))),
    'request': {'method': 'GET', 'url': '/', 'protocol': 'HTTP/1.1'},
    'status': '200',
    'useragent': user_agents 对象  # 使用 user_agents.browser 方法可解
}
```

使用示例：

```python
from apache_analysis import dispatcher, load
from apache_analysis import handler_status, user_agent

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

```

# 运行效果

状态码分析：

```shell

在 2017-07-05【 14:29:52 - 14:29:52 】内
                                         200 出现 1 次，占比 100%


在 2017-07-05【 14:29:52 - 14:30:06 】内
                                         200 出现 6 次，占比 100%


在 2017-07-05【 14:30:08 - 14:30:26 】内
                                         200 出现 5 次，占比 83%
                                         206 出现 1 次，占比 16%


在 2017-07-05【 14:30:29 - 14:30:45 】内
                                         200 出现 3 次，占比 75%
                                         206 出现 1 次，占比 25%


在 2017-07-05【 14:30:48 - 14:30:50 】内
                                         200 出现 3 次，占比 60%
                                         206 出现 2 次，占比 40%

```

浏览器版本分析：

```bash

截止：2017-07-17 09:19:27+08:00
            客户端：Chrome               版本：57.0.2987       出现次数：4405
            客户端：Chrome               版本：58.0.3029       出现次数：1517
            客户端：Chrome               版本：56.0.2924       出现次数：1434
            客户端：IE                   版本：6.0             出现次数：921
            客户端：Chrome               版本：45.0.2454       出现次数：865
            客户端：IE                   版本：11.0            出现次数：848
            客户端：Baiduspider          版本：2.0             出现次数：831
            客户端：Sogou Explorer       版本：1.0             出现次数：756
            客户端：Firefox              版本：52.0            出现次数：693
            客户端：Chrome               版本：50.0.2661       出现次数：660
            客户端：Chrome               版本：49.0.2623       出现次数：624
            客户端：Firefox              版本：50.0            出现次数：496
            客户端：Chrome               版本：55.0.2883       出现次数：467
            客户端：Chrome               版本：43.0.2357       出现次数：358
            客户端：QQ Browser           版本：9.5.10219       出现次数：351
            客户端：Firefox              版本：53.0            出现次数：312
            客户端：YandexBot            版本：3.0             出现次数：283
            客户端：Safari               版本：10.0.2          出现次数：274
            客户端：QQ Browser Mobile    版本：6.2             出现次数：272
            客户端：Mobile Safari UI/WKWebView 版本：                出现次数：230
            客户端：UC Browser           版本：6.1.2107        出现次数：217
            客户端：QQ Browser           版本：9.6.10872       出现次数：208
            客户端：Chrome               版本：59.0.3071       出现次数：202
            客户端：Chrome               版本：31.0.1650       出现次数：177
            客户端：QQ Browser           版本：9.6.11372       出现次数：171
            客户端：Mobile Safari        版本：8.0             出现次数：168
            客户端：Safari               版本：10.1            出现次数：148
            客户端：IE                   版本：8.0             出现次数：143
            客户端：Chrome               版本：54.0.2840       出现次数：125
            客户端：Chrome               版本：51.0.2704       出现次数：122
            客户端：Baiduspider-render   版本：2.0             出现次数：122
            客户端：Safari               版本：10.0.3          出现次数：116
            客户端：Mobile Safari        版本：9.0             出现次数：98
            客户端：UC Browser           版本：6.1.2716        出现次数：89
            客户端：Chrome Mobile        版本：57.0.2987       出现次数：84
            客户端：Opera                版本：45.0.2552       出现次数：78
            客户端：Edge                 版本：14.14393        出现次数：75
            客户端：QQ Browser           版本：9.0.2524        出现次数：71
            客户端：Firefox              版本：54.0            出现次数：66
            客户端：Chrome               版本：47.0.2526       出现次数：49
            客户端：Safari               版本：10.0.1          出现次数：46
            客户端：Maxthon              版本：5.0             出现次数：45
            客户端：Chrome               版本：39.0.2171       出现次数：45
            客户端：Firefox              版本：24.0            出现次数：40
            客户端：Chrome               版本：60.0.3080       出现次数：38
            客户端：UC Browser           版本：11.5.7          出现次数：30
            客户端：Mobile Safari        版本：10.0            出现次数：29
            客户端：IE                   版本：9.0             出现次数：28
            客户端：Android              版本：5.0.2           出现次数：26
            客户端：QQ Browser Mobile    版本：7.2             出现次数：22
            客户端：Other                版本：                出现次数：19
            客户端：Android              版本：5.1             出现次数：15
            客户端：Mobile Safari        版本：5.0.2           出现次数：14
            客户端：Chrome Mobile        版本：42.0.2307       出现次数：13
            客户端：Apple Mail           版本：602.4.6         出现次数：13
            客户端：UC Browser           版本：1.0.0           出现次数：13
            客户端：MobileSafari         版本：602.1           出现次数：12
            客户端：Chrome               版本：35.0.1916       出现次数：10
            客户端：Firefox Beta         版本：3.0.b4          出现次数：7
            客户端：IE                   版本：7.0             出现次数：7
            客户端：Android              版本：5.1.1           出现次数：6
            客户端：AOL                  版本：9.5.4337        出现次数：6
            客户端：UC Browser           版本：11.4.8          出现次数：6
            客户端：Chrome Mobile WebView 版本：38.0.0          出现次数：6
            客户端：Chrome Mobile WebView 版本：45.0.2454       出现次数：6
            客户端：Chrome               版本：19.0.1036       出现次数：4
            客户端：Chrome               版本：17.0.963        出现次数：4
            客户端：Chrome Mobile WebView 版本：35.0.1916       出现次数：4
            客户端：Opera                版本：11.52           出现次数：3
            客户端：Kazehakase           版本：0.4.5           出现次数：3
            客户端：Firefox              版本：3.0             出现次数：3
            客户端：Chrome Mobile WebView 版本：33.0.0          出现次数：3
            客户端：QQ Browser Mobile    版本：6.9             出现次数：3
            客户端：Arora                版本：0.3             出现次数：3
            客户端：MiuiBrowser          版本：8.6.5           出现次数：2
            客户端：bingbot              版本：2.0             出现次数：2
            客户端：Android              版本：4.2.1           出现次数：2
            客户端：Kazehakase           版本：0.5.6           出现次数：1
            客户端：QQ Browser           版本：9.5.10548       出现次数：1
            客户端：Mobile Safari        版本：6.0             出现次数：1
```


