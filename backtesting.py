import pandas as pd
import numpy as np
from data_reader import DataReader
from strategy import My_Strategy
from datetime import datetime

class Backtesting:
    #这是一个专门用于回测的类
    def __init__(self,daily_data,start_money,stock_list,
                 date_list,stock_moneylist,
                 signal_list,start_time,end_time):
        self.daily_data=daily_data           #获取按日期的数据
        self.daily_data.set_index(['stk_id', 'date'], inplace=True)#设置股票代码和日期为索引
        self.start_money=start_money         #获取初始资金
        self.stock_list=stock_list           #获取股票列表
        self.date_list=date_list             #获取日期列表
        self.stock_money=stock_moneylist     #资产配置字典，key为股票代码，value为该股票的资产

        self.signal=signal_list              #信号字典，key为股票代码，value为该股票的信号
                                             #为一个嵌套列表，列表中的元素为[日期+信号+数量]，数量为'full'表示满仓买卖
        self.start_time=start_time           #获取回测开始时间 
        self.end_time=end_time               #获取回测结束时间
        self.yongjin_rate=0.001              #佣金费率，默认为0.001
        self.yinhua_tax_rate=0.001           #印花税率，默认为0.001
        self.guohu_tax_rate=0.002            #过户费率，默认为0.002
        self.profit={}                       #收益字典，key为股票代码，value为该股票的收益
                                             #为一个嵌套列表，列表中的元素为日期+收益
        self.profit_sum={}                   #收益汇总字典，key为股票代码，value为该股票的收益汇总
        self.profit_sum_list=[]              #收益汇总列表，列表中的元素为每天的收益汇总
        self.stock_number={}                 #股票持有量字典，key为股票代码，value为该股票的持有量        
                                             #为一个嵌套列表，列表中的元素为日期+当日的持有量
        self.logger_stock={}                 #日志字典，key为股票代码，value为该股票的日志
                                             #为一个嵌套列表，列表中的元素为日期+当日的日志
        self.logger_date=[]                  #日志列表，列表中的元素为每天的日志
        
    def trade_by_signal(self):
        #根据信号进行交易,记录下每个时刻的收益和每个时刻的持仓
        start_date = datetime.strptime(self.start_time, '%Y-%m-%d')
        end_date = datetime.strptime(self.end_time, '%Y-%m-%d')
        for stock in self.stock_list:
            #遍历每只股票，对每只股票进行交易
            money=self.stock_money[stock]#设置该股票的初始资产
            for stock_signal in self.signal[stock]:
                #遍历每只股票的信号，对每只股票进行交易，stock_signal为[日期+信号+数量]
                temp_date=stock_signal[0]
                temp_signal=stock_signal[1]
                temp_number=stock_signal[2]
                if temp_signal==1:
                    #如果信号为1，即买入信号
                    self.buy_stock(stock,temp_date,temp_number)
                elif temp_signal==-1:
                    #如果信号为-1，即卖出信号
                    self.sell_stock(stock,temp_date,temp_number)

    def buy_stock(self,stock,date,number):
        #stock是股票名字
        #date是日期
        #number是买入数量
        
        price=self.daily_data.loc[(stock,date),'close']#获取当日收盘价
        if number=='full':
            #如果买入数量为'full'，即满仓买入,则买入数量为该股票的最大买入数量,但是要算上手续费
            number=money/(price*(1+self.yongjin_rate+self.yinhua_tax_rate+self.guohu_tax_rate))

        #计算手续费
        fee=price*number*(self.yongjin_rate+self.yinhua_tax_rate+self.guohu_tax_rate)
        #买入股票
        pass
    def sell_stock(self,stock,date,number):
        #卖出股票
        pass
    def set_fee_rate(self,yongjin_rate,yinhua_tax_rate,guohu_tax_rate):
        #通过外界参数获取各个手续费率
        self.yongjin_rate=yongjin_rate
        self.yinhua_tax_rate=yinhua_tax_rate
        self.guohu_tax_rate=guohu_tax_rate

    
