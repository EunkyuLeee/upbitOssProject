# 시연용 backTesting
from dataPrepare import prepareData
from predictModel import trendPredictModel
import matplotlib.pyplot as plt

def backTesting():
    df = prepareData()
    temp = df
    # 보유여부
    df.loc[df['signal'].shift(1) == True & (trendPredictModel(temp)), 'holding'] = True # 매수
    df.loc[df['signal'].shift(1) == False & (trendPredictModel(temp)), 'holding'] = False   # 매도
    df['holding'].ffill(inplace=True)
    df['holding'].fillna(False, inplace=True)


    # 보유수익률

    df['holding_rev'] = df.loc[df['holding'] == True, 'daily_rev']
    df['holding_rev'].fillna(1, inplace=True)

    df['rsi_rev'] = df['holding_rev'].cumprod()
    df['just_holding_profit'] = df['close']/df.iloc[0, 0]

    return df 

df = backTesting()

print("==============df================")
print(df)

# plot draw
plt.rcParams['figure.dpi'] = 200
df[['rsi_rev', 'just_holding_profit']].plot(figsize=(8, 4))
plt.show()