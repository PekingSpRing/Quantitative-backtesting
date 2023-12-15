import pandas as pd
from data_reader import DataReader
import numpy as np

class Your_strategy:
    def __init__(self,daily_data,start_money,stock_list,date_list):
        self.daily_data=daily_data   #获取按日期的数据
        self.start_money=start_money #获取初始资金
        self.stock_list=stock_list   #获取股票列表
        self.date_list=date_list     #获取日期列表
        self.stock_money={}          #资产配置字典，key为股票代码，value为该股票的资产
        self.stock_number={}         #股票持有量字典，key为股票代码，value为该股票的持有量

    def Your_get_stock_money(self):
        ################################

        # 请在这里实现你初始资产配置策略 
        # 请注意，你的策略需要返回一个字典，字典的key为股票代码，value为该股票的资产

        ################################
        return self.stock_money
    
    def Your_get_signal(self):
        ################################

        # 请在这里实现你信号生成策略 
        # 请注意，你的策略需要返回一个字典，字典的key为股票代码，value为该股票的信号
        # 信号为一个列表，列表中的元素为每天的信号，1为买入，-1为卖出，0为不操作

        ################################
        return self.signal