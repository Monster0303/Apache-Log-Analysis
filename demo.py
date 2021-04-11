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
