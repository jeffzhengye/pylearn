"""
Created on Thu May 13 23:02:01 2021

@author: Great World
"""
import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# import re

start_day = '2020-01-01'
start_dat_2 = start_day[0:4] + start_day[5:7] + start_day[8:10]
end_day = None

# code_list_df = read_excel('')
code_list = ['000002', '300759']

'''
最重要的问题是要解决个股停牌的数据缺失
解决方法如下：
创建几个个df分别存放计算指数需要的数据（如市值、价格、成交量）
其index是不会停牌的指数的日期
在这个index里存放全部股票的数据，向前填充缺失数据 ffill
然后用这个df来计算我们指数的结果
'''

# 大盘历史数据，用于提取所有交易日的日期作为df的index
sh_index_daily_df = ak.stock_zh_index_daily(symbol="sh000001")  # get data
sh_index_daily_df = sh_index_daily_df[
    sh_index_daily_df.index >= datetime(start_day)]  # select data
df_index = sh_index_daily_df.index



# 存放每只股票各种数据的df
price_df = pd.DataFrame(index=df_index)
market_value_df = pd.DataFrame(index=df_index)
value_ratio_df = pd.DataFrame(index=df_index)
vol_df = pd.DataFrame(index=df_index)
outcome_index = pd.DataFrame(index=df_index)

# 从akshare接口获得个股的市值、价格等计算指数需要的数据
for code in code_list:
    if str(code)[0:2] == '60' or str(code)[0:2] == '68':
        code = 'sh' + code
    else:
        code = 'sz' + code
    stock_df = ak.stock_zh_a_daily(
        symbol=code, start_date=start_dat_2, adjust="qfq")
    price_df.insert(0, code, stock_df['close'])
    market_value_df.insert(
        0, code, stock_df['outstanding_share'] * stock_df['close']
    )  # 流通股*收盘价=流通市值
    vol_df.insert(0, code, stock_df['volume'])
market_value_df['sum'] = market_value_df.sum(axis=1)

# 补全缺失数据
price_df = price_df.ffill()
market_value_df = market_value_df.ffill()
vol_df = vol_df.ffill()

'''
每个成分股的份额占总份额的比例 乘以成分股的收盘价 
其和就是指数当天的的值

如果要换算法，比如用成交量作为权重，或者权重平均
只需修改这部分的算法即可 
'''

for code in code_list:
    if str(code)[0:2] == '60' or str(code)[0:2] == '68':
        code = 'sh' + code
    else:
        code = 'sz' + code
    value_ratio_df.insert(0, code, market_value_df[code] / market_value_df['sum'])
    outcome_index.insert(0, code, value_ratio_df[code] * price_df[code])

outcome_index['sum'] = outcome_index.sum(axis=1)  # 指数的值

# Plot
left = 0.037
width = 0.938
bottom = 0.055
height = 0.9
rect_line = [left, bottom, width, height]
fig1 = plt.figure(figsize=(18, 9))
ax0 = fig1.add_axes(rect_line)
ax0.plot(outcome_index['sum'])