import pandas as pd
from data_reader import DataReader
import numpy as np
from design_strategy import Your_strategy
import json
import datetime

class My_Strategy:
    def __init__(self,daily_data,start_money,stock_list,date_list):
        self.special_stregy=Your_strategy(daily_data,start_money,stock_list,date_list)

        self.daily_data=daily_data   #获取按日期的数据
        self.start_money=start_money #获取初始资金
        self.stock_list=stock_list   #获取股票列表
        self.date_list=date_list     #获取日期列表
        print(date_list)             #!!!!!!!!! 这里看一下日期是不是按顺序排列的
        self.stock_money={}          #资产配置字典，key为股票代码，value为该股票的资产
        self.stock_number={}         #股票持有量字典，key为股票代码，value为该股票的持有量
        self.signal={}               #信号字典，key为股票代码，value为该股票的信号
                                     #为一个列表，列表中的元素为每天的信号，1为买入，-1为卖出，0为不操作
        self.real_money={}           #当前的总价值字典，key为股票代码，value为目前手里所有股票+现金的总价值
                                     #value为一个嵌套列表，列表中的元素为日期+总价值
        self.start_time=date_list[0] #获取回测开始时间  第一天和最后一天是默认值，后面可以修改
        self.end_time=date_list[-1]  #获取回测结束时间

        self.reverse_time=22         #反转因子的时间窗口,默认为22天
        self.reverse_rate=0.05        #反转因子的阈值,默认为0.05

    
    def get_stock_money(self,choice='default'):
        #对每只股票进行资产配置，返回一个字典，key为股票代码，value为该股票的资产
        if choice=='default':
            #默认情况下，choice='default'，每只股票的资产配置为初始资金除以股票数量
            sigle_money=self.start_money/len(self.stock_list)
            for stock in self.stock_list:
                self.stock_money[stock]=[]
                self.stock_money[stock].append(['before start',self.start_money/len(self.stock_list)])
                self.stock_number[stock]=[] #顺便初始化一下股票持有量字典
                self.stock_money[stock].append(['before start',0])#最开始每个股票的持有量都是0
                self.real_money[stock]=[]#顺便初始化一下总价值字典
                self.real_money[stock].append(['before start',self.start_money/len(self.stock_list)])
                
        elif choice=='by_market_cap':
            #按照市值进行资产配置，但是我还没想好
            print("第二种资产配置方式我还没想好")
        elif choice=='design':
            #按照自己的策略进行资产配置
            self.stock_money=self.special_stregy()
        return self.stock_money
    
    def get_signal(self,choice='default',path='null'):
        #对每只股票进行信号生成，返回一个字典，key为股票代码，value为该股票的信号
        start_date = datetime.strptime(self.start_time, '%Y-%m-%d')
        end_date = datetime.strptime(self.end_time, '%Y-%m-%d')
        if choice=='default':
            #默认情况下，choice='default'，就是一个寻常的反转因子策略
            for stk_id, data in self.daily_data.groupby('stk_id'):
                self.signal[stk_id] = []
                for date, row in data.iterrows():
                    date=datetime.strptime(date, '%Y-%m-%d')
                    if start_date <= date <= end_date:
                        mean_price = data.loc[data.index < date, 'close'].tail(self.reverse_time).mean()
                        current_price = row['close']
                        # 生成交易信号
                        if current_price > mean_price * (1 + self.reverse_rate):
                            signal = -1  # 卖出信号
                        elif current_price < mean_price * (1 - self.reverse_rate):
                            signal = 1  # 买入信号
                        else:
                            signal = 0  # 不操作
                        self.signal[stk_id].append([date, signal,'full']) #full表示满仓买卖
                        #有一种情况是出现连续买入的情况[1,1,1,1,1,-1,-1,-1]由于每次都是满仓操作
                        #所以会出现连续买入的情况，这种情况在后面的回测中会进行处理，不必担心                    
        elif choice=='fromfiles':
            if path=='null':
                print("你选择了从文件中读取信号，但是没有给出文件路径")
            else:
                self.signal=json.load(open(path,'r'))#从path文件中读取信号
            #你可以将一个json格式的文件作为信号输入
            print("json格式的文件这部分还没写好")
        elif choice=='design':
            #按照自己的策略进行信号生成
            self.signal=self.Your_get_signal()
        return self.signal
    
    def set_time_block(self,start_day,end_day):
        #设置回测的时间段,格式必须是：2020-01-02 这样的字符串
        self.start_time=start_day
        self.end_time=end_day
    
    def save_signal(self,path):
        #将信号保存到文件中
        json.dump(self.signal,open(path,'w'))

