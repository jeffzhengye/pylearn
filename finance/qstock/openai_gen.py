import openai
from retrying import retry

openai.api_key = ""

@retry(stop_max_attempt_number=10, wait_fixed=1000 * 10)
def chat_openai(message: str):
    """docs: https://platform.openai.com/docs/api-reference/chat/create?lang=python

    Args:
        message (str): _description_

    Returns:
        _type_: _description_
    """
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  #  Currently, only gpt-3.5-turbo and gpt-3.5-turbo-0301 are supported.
        temperature=0.7, #  between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
        max_tokens=256,
        top_p=1,
        messages=[
            {"role": "system", "content": "你是一个股票专家"},
            {"role": "user", "content": message}
        ]
    )
    # print(completion.choices[0].message, type(completion.choices[0].message))
    return completion.choices[0].message['content']


@retry(stop_max_attempt_number=10, wait_fixed=1000 * 2)
def qs_ths_index_name(sector: str):
    return qs.ths_index_member(sector)
    

@retry(stop_max_attempt_number=10, wait_fixed=1000 * 2)
def qs_ths_index_member():
    return qs.ths_index_member()


prompt = """
写一个股票推荐，要求写出股票名：机器人 (股票代码: 300024)，买入点位: 12.19元，目标价位: 13.15元，50个字以内的推荐理由. 输出格式三行第一行股票名，第二行买入点位和目标价，第三行推荐理由。
"""

# 讯飞prompt
prompt = """写一个股票推荐，要求写出股票名：新华网 (股票代码: 603888)，买入点位: 32.02元和推荐理由。 输出格式第一行关注：建议抢购或关注的理由（不多于15个字,比如“航空航天领军企业，又一波利好，建议抢购！”）,第二行：股票名（如：中国航空（股票代码：601111）），第三行：买入点位（如：买入点位：48.17元），第四行买入建议：（根据行业写10个字以内的买入建议（如：看好金融行业的前景）)。"""

# 写一个股票推荐，要求写出股票名：登康口腔 (股票代码: 001328)，板块:医疗健康, 买入点位: 34.79元和推荐理由。 输出格式第一行：建议抢购或关注的理由（不多于15个字,比如“航空航天领军企业，又一波利好，建议抢购！”)
# 第二行：股票名（如：中国航空（股票代码：601111））
# 第三行：买入点位（如：买入点位：48.17元）
# 第四行：根据行业板块写20个字以内的买入建议（如：大盘股回调后短期报复性回升  个股目前形态上来看 没有问题 底部建仓  震荡拉升）。

# 龙虎榜
        # prompt = f"""写一个股票推荐，要求写出股票名：{row['股票名称']} (股票代码: {row['股票代码']})，板块:{sector},买入点位: {row['收盘价']}元和推荐理由。\n输出格式第一行：建议抢购或关注的理由（不多于15个字,比如“航空航天领军企业，又一波利好，建议抢购！”）\n第二行：股票名（如：中国航空（股票代码：601111））\n第三行：买入点位（如：买入点位：48.17元）\n第四行：根据行业写10个字以内的买入建议（如：大盘股回调后短期报复性回升  个股目前形态上来看 没有问题 底部建仓  震荡拉升）。"""
        

import qstock as qs
import time

def gen_billboard(df, sector_k, sector='', top_k=20) -> None:
    # df=qs.stock_billboard(start=None, end=None)
    end_k = (sector_k + 1 ) * top_k
    # i = 0
    i = top_k * sector_k
    recomands = []
    for idx, row in df.iterrows():
        
        # if i < 10:
        #     i += 1
        #     continue
        
        prompt = f"""写一个股票推荐，要求写出股票名：{row['名称']} (股票代码: {row['代码']})，板块:{sector},买入点位: {row['现价']}元和推荐理由。\n输出格式第一行：建议抢购或关注的理由（不多于15个字,比如“航空航天领军企业，又一波利好，建议抢购！”）\n第二行：股票名（如：中国航空（股票代码：601111））\n第三行：买入点位（如：买入点位：48.17元）\n第四行：根据行业写10个字以内的买入建议（如：大盘股回调后短期报复性回升  个股目前形态上来看 没有问题 底部建仓  震荡拉升）。"""
        
        if i % 2 == 0: # 奇数
            # print(i, 'prompt:', prompt)
            start_id = i // 2 + 1
            recommand = chat_openai(prompt)
            recomands.append(recommand)
            print(f"{start_id}. {recommand}")
        else:
            # print(i, 'prompt:', prompt)
            recommand = chat_openai(prompt)
            recomands.append(recommand)
            print(f"{recommand} 点赞关注！\n")
            # print(f"点赞关注!")
            # break
            
        i += 1
        if i >= end_k:
            break
        time.sleep(7)


# 振江股份（603507）高收盘，第二天开盘有概率会有一波洗盘要稳住，行情走势一片好
# 东方日升（300118）底开短涨走势稳定，开盘上涨潜力股
# 代码	名称	现价	涨跌幅	涨速	换手	量比	振幅	成交额(亿)	流通股(亿)	流通市值(亿)	市盈率
# 根据以下股票今天行情，写一个一行的收评。中船防务 (股票代码: 600685), 现价30.81,涨跌幅10.0,涨速10.0,换手5.99,量比1.7,振幅11.82
# 要求1：输出例子1：振江股份（603507）高收盘，第二天开盘有概率会有一波洗盘要稳住，行情走势一片好!输出例子2：东方日升（300118）底开短涨走势稳定，开盘上涨潜力股
# 要求2：不要输出换手、量比、收盘价等数据，只对数字就行总结，50个字左右。

# 根据以下股票今天行情，写一个一行的收评。中船防务 (股票代码: 600685), 现价30.81,涨跌幅10.0,涨速10.0,换手5.99,量比1.7,振幅11.82
# 要求1：输出形式：振江股份（603507）高收盘，第二天开盘有概率会有一波洗盘要稳住，行情走势一片好!
# 要求2：不要输出换手、量比、收盘价等数据，只对数字就行总结，40个字左右。
# 要求3：输出股票代码

# 根据以下股票今天行情，写一个一行的收评。奥泰生物 (股票代码: 688606),概念板块：猴痘概念,现价99.7元,涨跌幅2.51%,涨速-0.09,换手0.98%,量比2.05,振幅3.4%。
# 要求1：输出形式：振江股份（603507）高收盘，第二天开盘有概率会有一波洗盘要稳住，行情走势一片好!
# 要求2：不要输出换手、量比、收盘价等数据，只对数字就行总结，40个字左右。
# 要求3：输出股票代码

    #   prompt = f"""根据以下股票今天行情，写一个一行的收评。{row['名称']} (股票代码: {row['代码']}), 现价{row['现价']},涨跌幅{row['涨跌幅']},涨速{row['涨跌幅']},换手{row['换手']},量比{row['量比']},振幅{row['振幅']}\n输出例子如下：例子1：振江股份（603507）高收盘，第二天开盘有概率会有一波洗盘要稳住，行情走势一片好!例子2：东方日升（300118）底开短涨走势稳定，开盘上涨潜力股
    #     """


def gen_concept_closing(df, sector: str, top_k=10):
    import qstock as qs 
    # flag='概念板块' or '行业板块'
    #行业板块名称
    # name_list=qs.ths_index_name('概念')
    # #查看5个

    # df=qs.ths_index_member(name_list[0])


    # import time
    # print(df.head())

    i = 0
    for idx, row in df.iterrows():
        # if i < 10:
        #     i += 1
        #     continue
        
        prompt = f"""根据以下股票今天行情，写一个一行的收评。{row['名称']} (股票代码: {row['代码']}),概念板块：{sector},现价{row['现价']}元,涨跌幅{row['涨跌幅']}%,涨速{row['涨速']},换手{row['换手']}%,量比{row['量比']},振幅{row['振幅']}%。\n要求1：输出形式：振江股份（603507）高收盘，第二天开盘有概率会有一波洗盘要稳住，行情走势一片好!\n要求2：不要输出换手、量比、收盘价等数据，只对数字就行总结，40个字左右。\n要求3：输出股票代码
        """
        # print(prompt)
        # break

        if i % 2 == 0: # 奇数
            # print(i, 'prompt:', prompt)
            start_id = i // 2 + 1
            print(f"{chat_openai(prompt)}")
        else:
            # print(i, 'prompt:', prompt)
            print(f"{chat_openai(prompt)}\n")
            # print(f"点赞关注!")
            # break
            
        i += 1
        if i > top_k:
            break
        time.sleep(7)

def get_closing_by_concept_row(row, sector):
    prompt = f"""根据以下股票今天行情，写一个一行的收评。{row['名称']} (股票代码: {row['代码']}),概念板块：{sector},现价{row['现价']}元,涨跌幅{row['涨跌幅']}%,涨速{row['涨速']},换手{row['换手']}%,量比{row['量比']},振幅{row['振幅']}%。\n要求1：输出形式：振江股份（603507）高收盘，第二天开盘有概率会有一波洗盘要稳住，行情走势一片好!\n要求2：不要输出换手、量比、收盘价等数据，只对数字就行总结，40个字左右。\n要求3：输出股票代码
        """
    return chat_openai(prompt)



def closing_gen():
    name_list=qs.ths_index_name('概念')
    name_list.remove("首发新股")
    for sector in name_list[:10]:
        df = qs.ths_index_member(sector)
        gen_concept_closing(df, sector=sector, top_k=20)
        
def opening_gen(concept_start=0, concept_end=20, top_k=20):
    name_list=qs_ths_index_name('概念')
    name_list.remove("首发新股")
    recommends = []
    for k, sector in enumerate(name_list[concept_start:concept_end]):
        df = qs_ths_index_member(sector)
        recommends.extend(gen_billboard(df, sector_k=k, sector=sector, top_k=top_k))
    return recommends

# closing_gen()
# opening_gen()