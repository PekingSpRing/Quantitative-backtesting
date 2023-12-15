import pandas as pd
import numpy as np

class DataReader:
    def __init__(self, path):
        self.path = path
        self.data=pd.read_feather(path)
        #self.data.to_csv('data/'+path.split('/')[1].split('.')[0]+'.csv',index=False)
        #存一下csv文件，直观的感受一下数据样子

    def drop_discrete_data(self):
        # 删除离散数据
        # 获取最全面的日期范围
        complete_dates = self.data['date'].drop_duplicates().sort_values().reset_index(drop=True)

        # 筛选出完整记录的股票
        # 使用 groupby 和 filter 函数来实现
        complete_stocks = self.data.groupby('stk_id').filter(lambda x: complete_dates.isin(x['date']).all())

        # 保存处理后的数据
        complete_stocks_reset=complete_stocks.reset_index(drop=True)
        complete_stocks_reset.to_feather('data/stk_daily.feather')
        complete_stocks_reset.to_csv('data/new_stk_daily.csv',index=False)

        # 获取股票名称的唯一值列表
        unique_stocks = complete_stocks['stk_id'].unique().tolist()

        # 返回股票列表和日期列表
        return unique_stocks,complete_dates

if __name__ == '__main__':
    stk_daily=DataReader('raw_data/stk_daily.feather')
    all_stocks,all_dates=stk_daily.drop_discrete_data()
    #stk_fin_annotation=DataReader('raw_data/stk_fin_annotation.feather')
    #stk_fin_balance=DataReader('raw_data/stk_fin_balance.feather')
    #stk_fin_cashflow=DataReader('raw_data/stk_fin_cashflow.feather')
    #stk_fin_income=DataReader('raw_data/stk_fin_income.feather')
    #stk_fin_item_map=DataReader('raw_data/stk_fin_item_map.feather')
    #stk_daily.drop_discrete_data()
        