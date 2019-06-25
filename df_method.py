import pandas as pd
import numpy as np
import math

# 対数表記での増減率を求めるメソッド
def rise_fall_rate(df, x_days_later):
    # すべての要素の対数をとり100倍する
    df = df.apply(np.log)*100 # applyはすべての要素に関数を適用するメソッド    
    # 特定の日数後の増減を求める
    df = df.diff(x_days_later)
    # 特定の日数分の行を削除
    df = df.drop(df.index[0:x_days_later], axis=0)
    return df

# 移動平均線を求めるメソッド
def moving_average(df, day):
    # すべての要素の対数をとり100倍する
    df = df.apply(np.log)*100
    # 移動平均を求める
    df = df.rolling(window=day, min_periods=day).mean()
    # 特定の日数分の行を削除
    df = df.drop(df.index[0:day-1], axis=0) 
    return df

# デッドクロスとゴールデンクロスを求めるメソッド
def GCDC(df, short, long):
    # 移動平均を求める
    mv1 = moving_average(df, short)#短期
    mv2 = moving_average(df, long)#長期
    # 差を求める
    mv_diff = mv1 - mv2
    # いらない部分を削る
    mv_diff = mv_diff.drop(mv_diff.index[0:long-short], axis=0)
    return mv_diff

# データフレームをシフトさせるメソッド
def df_shift(df, day):
    df = df.shift(day)
    df = df.drop(df.index[0:day], axis=0)
    return df

# リストに経済指標を入れるメソッド
def add_data(csv_name, x_days_later):
    df = pd.read_csv(csv_name, index_col='Date', parse_dates=True)
    df = rise_fall_rate(df, x_days_later)
    return df

# RSIを返すメソッド
def RSI(df):
    df = df.diff(1) # 前日からの変動を求める
    df = df[1:] # 先頭行を削除
    up, down = df.copy(), df.copy()
    up[up < 0] = 0 # 0未満の値を0にする
    down[down > 0] = 0 # 0超過の値を0にする
    up_sma_14 = up.rolling(window=14, center=False).mean() # 移動平均を求める
    down_sma_14 = down.abs().rolling(window=14, center=False).mean() # 絶対値をとって移動平均を求める
    up_sma_14 = up_sma_14 / 14
    down_sma_14 = down_sma_14 / 14
    RSI = up_sma_14 / (up_sma_14 + down_sma_14) * 100
    RSI = RSI[13:]
    #RS = up_sma_14 / down_sma_14
    #RSI = 100.0 - (100.0 / (1.0 + RS))
    return RSI

# 標準化
def Z_score_normalization(df):
    return df

def Min_Max_normalization(df):
    return df