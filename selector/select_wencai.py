"""
https://www.iwencai.com/
"""
import datetime
import pywencai
# from selector.select_queries import *

select_query = "中证500成分股，非ST，非科创，MACD金叉，按价格从小到大"  # 这里自定义问财选股的问句prompt
print('选股问句：', select_query, '\n')


def get_wencai_codes_prices(query, debugging=False) -> dict[str, str]:
    df = pywencai.get(query=query)

    if df is not None and type(df) is not dict and df.shape[0] > 0:
        possible_price_columns = [
            '现价(元)',
            '最新价',
            f'收盘价:不复权[{datetime.datetime.now().strftime("%Y%m%d")}]',
            f'收盘价:不复权(元)[{datetime.datetime.now().strftime("%Y%m%d")}]',
        ]

        target_col = None

        for temp_col in possible_price_columns:
            if temp_col in df.columns:
                target_col = temp_col
                break

        if target_col is None:
            return {}

        df['curr_price'] = df[target_col].astype(float)
        if debugging:
            now = datetime.datetime.now()
            # now_day = now.strftime("%Y-%m-%d")
            # now_min = now.strftime("%H:%M")
            print(f'Wencai: {now.strftime("%H:%M:%S")}\n', df[['股票代码', '股票简称', 'curr_price']])
        return df.set_index('股票代码')['curr_price'].to_dict()
    return {}


if __name__ == '__main__':
    a = get_wencai_codes_prices([select_query], debugging=True)
    print(a)
    i = 0
    for k in a:
        i += 1
        print(i, '\t', k, '\t', a[k])
