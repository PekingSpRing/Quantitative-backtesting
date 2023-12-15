import pandas as pd
import numpy as np
from data_reader import DataReader
from strategy import My_Strategy
from datetime import datetime

class Backtesting:
    #这是一个专门用于回测的类
    def __init__(self,daily_data,start_money,stock_list,
                 date_list,start_stock_moneylist,
                 signal_list,start_time,end_time):
        self.daily_data=daily_data           #获取按日期的数据
        self.daily_data.set_index(['stk_id', 'date'], inplace=True)#设置股票代码和日期为索引
        self.start_money=start_money         #获取初始资金
        self.stock_list=stock_list           #获取股票列表
        self.date_list=date_list             #获取日期列表
        self.start_stock_money=start_stock_moneylist     #资产配置字典，key为股票代码，value为该股票的资产
        self.signal=signal_list              #信号字典，key为股票代码，value为该股票的信号
                                             #为一个嵌套列表，列表中的元素为[日期+信号+数量]，数量为'full'表示满仓买卖
        self.start_time=start_time           #获取回测开始时间 
        self.end_time=end_time               #获取回测结束时间
        
        
        self.stock_number={}                 #股票持有量字典，key为股票代码，value为该股票的持有量        
                                             #为一个嵌套列表，列表中的元素为日期+当日的持有量
        
        self.stock_money={}                  #股票资产字典，key为股票代码，value为该股票的资产
                                             #为一个嵌套列表，列表中的元素为日期+当日手里有的现金  
        
        self.net_value={}                       #按股票的净值收益字典，key为股票代码，value为该股票的收益
                                             #为一个嵌套列表，列表中的元素为日期+净值收益
        self.net_value_day={}                   #总净值收益列表，列表中的元素为每天的总净值收益
        
        self.real_money={}                   #当前的总价值字典，key为股票代码，value为目前手里所有股票+现金的总价值
                                             #value为一个嵌套列表，列表中的元素为日期+总价值
        
        self.real_money_day={}               #当前的总价值字典，key为日期，value为目前手里所有股票+现金的总价值
        self.initialize_dict()               #初始化上面四个字典       
        
        self.logger_stock={}                 #日志字典，key为股票代码，value为该股票的日志
                                             #为一个嵌套列表，列表中的元素为日期+当日的日志
        self.logger_date=[]                  #日志列表，列表中的元素为每天的日志
        self.profit_sum_stock={}             #收益汇总字典，key为股票代码，value为该股票的收益汇总
        self.profit_sum_date=[]              #收益汇总列表，列表中的元素为每天的收益汇总                              
        


        self.yongjin_rate=0.001              #佣金费率，默认为0.001
        self.yinhua_tax_rate=0.001           #印花税率，默认为0.001
        self.guohu_tax_rate=0.002            #过户费率，默认为0.002
    
    def initialize_dict(self):
        #初始化各种字典，包括收益字典，每日总资产字典，股票持有量字典，现金字典
        for stock in self.stock_list:
            self.stock_number[stock]=[] #初始化一下股票持有量字典
            self.stock_number[stock].append(['before start',0])#最开始每个股票的持有量都是0

            self.stock_money[stock]=[] #初始化一下股票资产字典
            self.stock_money[stock].append(['before start',self.start_stock_money[stock]])#最开始每个股票的资产都是初始资金除以股票数量

            self.real_money[stock]=[] #初始化一下总价值字典
            self.real_money[stock].append(['before start',self.start_stock_money[stock]])#最开始每个股票的总价值都是初始资金除以股票数量

            self.net_value[stock]=[]#初始化一下净值收益字典
            self.net_value[stock].append(['before start',1])#最开始每个股票的收益都是1，就是没变嘛

            self.real_money_day['before start']=self.start_money#初始化一下每日总价值字典,最开始的净值就是初始资金
            self.net_value_day['before start']=1.0#初始化一下每日总净值,最开始的净值就是1
        
    def trade_by_signal(self):
        #根据信号进行交易,记录下每个时刻的收益和每个时刻的持仓
        start_date = datetime.strptime(self.start_time, '%Y-%m-%d')
        end_date = datetime.strptime(self.end_time, '%Y-%m-%d')
        for stock in self.stock_list:
            #遍历每只股票，对每只股票进行交易
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
                else:
                    #如果信号为0，即不操作
                    yesterday_money=self.stock_money[stock][-1][1]#获取该股票的当前资产,最后一个列表的第二个元素
                    yesterday_number=self.stock_number[stock][-1][1]#获取该股票的当前持有量,最后一个列表的第二个元素
                    self.stock_money[stock].append([temp_date,yesterday_money])
                    self.stock_number[stock].append([temp_date,yesterday_number])
                    price=self.daily_data.loc[(stock,temp_date),'close']#获取当日收盘价
                    self.real_money[stock].append([temp_date,yesterday_money+yesterday_number*price])
                    #虽然没有进行任何操作，但是依然要记录下每天的持仓和每天的总价值
                if temp_date not in self.real_money_day:
                    self.real_money_day[temp_date]=0
                self.real_money_day[temp_date]+=self.real_money[stock][-1][1]#交易完之后，计算本日的总价值
             
    def buy_stock(self,stock,date,sig_number):
        #stock是股票名字
        #date是日期，字符串形式
        #number是买入数量      
        price=self.daily_data.loc[(stock,date),'close']#获取当日收盘价
        money=self.stock_money[stock][-1][1]#获取该股票的当前资产,最后一个列表的第二个元素
        number=self.stock_number[stock][-1][1]#获取该股票的当前持有量,最后一个列表的第二个元素
        if sig_number=='full':
            #如果买入数量为'full'，即满仓买入,则买入数量为该股票的最大买入数量,但是要算上手续费
            buy_number=int(money/(price*(1+self.yongjin_rate+self.guohu_tax_rate)))
            #如果没钱了，那么自然buy_number为0，也无所谓
            cost=price*buy_number*(1+self.yongjin_rate+self.guohu_tax_rate)
            left_money=money-cost
            left_stock_number=number+buy_number
            self.stock_money[stock].append([date,left_money])
            self.stock_number[stock].append([date,left_stock_number])
            self.real_money[stock].append([date,left_money+left_stock_number*price])
            if buy_number!=0:
                #如果买入数量不为0，则记录下日志
                if stock not in self.logger_stock.keys():
                    self.logger_stock[stock]=[]
                self.logger_stock[stock].append([date,'buy '+stock+',number-'+buy_number,', price-',price])
                self.logger_date.append(date,'buy '+stock+',number-'+buy_number,', price-',price)
            #计算收益这一部分最后算吧，我记录下每一天的持仓和资金，就可以算收益了
            else:
                #如果买入数量为0，则说明没钱了，无所谓，日志不作记录
                return
        else:
            ######！！！！！！！！！！！！！！！！！！！！！################
            #如果你输入的是一个数字，那么就按照你的数字买入
            #这个地方待会再写
            ######！！！！！！！！！！！！！！！！！！！！！################
            pass

    def sell_stock(self,stock,date,sig_number):
        #卖出股票
        #stock是股票名字
        #date是日期，字符串形式
        #number是卖出数量
        price=self.daily_data.loc[(stock,date),'close']
        money=self.stock_money[stock][-1][1]
        number=self.stock_number[stock][-1][1]
        if sig_number=='full':
            #说明是满仓卖出
            sell_number=number
            get_money=price*sell_number*(1-self.yongjin_rate-self.yinhua_tax_rate-self.guohu_tax_rate)
            left_money=money+get_money
            left_stock_number=0
            self.stock_money[stock].append([date,left_money])
            self.stock_number[stock].append([date,left_stock_number])
            self.real_money[stock].append([date,left_money+left_stock_number*price])
            if sell_number!=0:
                #如果卖出数量不为0，则记录下日志
                if stock not in self.logger_stock.keys():
                    self.logger_stock[stock]=[]
                self.logger_stock[stock].append([date,'sell '+stock+',number-'+sell_number,', price-',price])
                self.logger_date.append(date,'sell '+stock+',number-'+sell_number,', price-',price)
            else:
                #如果卖出数量为0，则说明没股票了，无所谓，日志不作记录
                return
        else:
            ######！！！！！！！！！！！！！！！！！！！！！################
            #如果你输入的是一个数字，那么就按照你的数字卖出
            #这个地方待会再写
            ######！！！！！！！！！！！！！！！！！！！！！################
            pass
    
    def calculate_profit(self):
        #计算每只股票的收益
        for stock in self.real_money:
            #遍历每只股票
            for j in self.real_money[stock]:
                #列表里的每一个值，都是一个列表，第一个元素是日期，第二个元素是当日的总价值
                temp_date=j[0]
                temp_realmoney=j[1]
                temp_net_value=temp_realmoney/self.start_stock_money[stock]
                self.net_value[stock].append([temp_date,temp_net_value])#这样计算出了每只股票的净值收益
        for day in self.real_money_day:
            #遍历每一天,算出每一天的总净值收益
            temp_day_net_value=self.real_money_day[day]/self.start_money
            self.net_value_day[day]=temp_day_net_value

    def calculate_performance_metrics(self):
        #计算回测的各种性能指标
        pass

    def set_fee_rate(self,yongjin_rate,yinhua_tax_rate,guohu_tax_rate):
        #通过外界参数获取各个手续费率
        self.yongjin_rate=yongjin_rate
        self.yinhua_tax_rate=yinhua_tax_rate
        self.guohu_tax_rate=guohu_tax_rate

if __name__ == '__main__':
    #仅仅用于测试
    pass
