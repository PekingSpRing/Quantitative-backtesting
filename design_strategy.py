import pandas as pd
from data_reader import DataReader
import numpy as np

class Your_strategy:
    def __init__(self,daily_data,stock_list,date_list,start_money=100000000):

        self.daily_data=daily_data   #获取按日期的数据
        self.start_money=start_money #获取初始资金
        self.stock_list=stock_list   #获取股票列表
        self.date_list=date_list     #获取日期列表
        self.start_stock_money={}    #资产配置字典，key为股票代码，value为该股票的资产

        self.signal={}               #信号字典，key为股票代码，value为该股票的信号
                                     #为一个列表，列表中的元素为每天的信号，1为买入，-1为卖出，0为不操作
       
        self.start_time=date_list[0] #获取回测开始时间  第一天和最后一天是默认值，后面可以修改
        self.end_time=date_list[-1]  #获取回测结束时间

        self.reverse_time=22         #反转因子的时间窗口,默认为22天
        self.reverse_rate=0.05        #反转因子的阈值,默认为0.05
    
    def set_time_block(self,start_day,end_day):
        #设置回测的时间段,格式必须是：2020-01-02 这样的字符串
        self.start_time=start_day
        self.end_time=end_day

    def Your_get_stock_money(self):
        ################################

        # 请在这里实现你初始资产配置策略 
        # 请注意，你的策略需要返回一个字典，字典的key为股票代码，value为该股票的初始资产

        ################################
        return self.stock_money
    
    def Your_get_signal(self):
        ################################

        # 请在这里实现你信号生成策略 
        # 请注意，你的策略需要返回一个字典，字典的key为股票代码，value为该股票的信号
        # 信号为一个嵌套列表,大列表中的每个小列表格式为[日期,交易信号,数量]
        # 日期为'年-月-日格式'
        # 交易信号1为买入，-1为卖出，0为不操作
        # 数量如果是'full'表示全仓买卖，如果是整数就表示按整数买卖
        # {'stock name':[['2020-02-19',1,300],……],……}

        ################################
        return self.signal