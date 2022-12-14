'''
RSI-EMA 지표 산출, RNN 모델 훈련하기 전 필요한 데이터 셋을 pyupbit 모듈을 사용해 가져오고 
RSI-EMA 지수를 기존 데이터셋에 추가한다. 
'''

import matplotlib.pyplot as plt
import pyupbit   
BUY_THRESHOLD = 20
SELL_THRESHOLD = 75


'''
if fngindex == -1 : # default
        BUY_THRESHOLD = 20; SELL_THRESHOLD = 75 # default
    elif fngindex < 50:
        if delta > 10 and grad > 0:
            BUY_THRESHOLD = 20; SELL_THRESHOLD = 80
        elif delta > 10 and grad < 0:
            BUY_THRESHOLD = 40; SELL_THRESHOLD = 80
    else:
        if delta > 10 and grad > 0:
            BUY_THRESHOLD = 50; SELL_THRESHOLD = 80
        elif delta > 10 and grad < 0:
            BUY_THRESHOLD = 30; SELL_THRESHOLD = 80

'''
'''
공포탐욕지수가 상승장에서만 영향을 주는거로 하자.
탐욕장에서는 70정도로 하고 극탐욕이면 60으로 하자. (sellthreshold)
'''

# from predictModel import fngModel
# from getIndex import getGrad

 
def getBuythreshold(fng, grad):
    # 공포장이고 하락이면 buyThreshold 올린다.
    if fng < 20 and grad < 0:
        return 40
    return 20

def getSellthreshold(fng):
    if 75 > fng > 50:
        return 70
    elif fng >= 75:
        return 65
    return 80

from getIndex import getGrad
from greedy_fear_index import fear_last_6month
from predictModel import fngModel

def prepareData(itv='minute60'):

 
    # 근데 fngIndex는 미래의 거래를 판단하는건뎅...?
    # 이 Threshold는 계속 바뀌어야 하는데... 함수 형태로 해서 계속 불러야지
    
    df = pyupbit.get_ohlcv('KRW-BTC', interval=itv)
    df['delta'] = df['close'] - df['close'].shift(1)
    df.loc[df['delta'] >= 0, 'rise'] = df['delta']
    df.loc[df['delta'] < 0, 'decline'] = -df['delta'] # 변화량이 없을 경우 결측값이 발생한다.
    df = df.fillna(0) # 결측값을 0으로 매워준다.

    df['AU'] = df['rise'].ewm(span=12, adjust=False).mean() # 최근 12시간을 기준으로 RSI를 계산한다. 
    df['DU'] = df['decline'].ewm(span=12, adjust=False).mean()
    df['RSI'] = df['AU'] / (df['AU'] + df['DU']) * 100

    df = df.iloc[11:] # 12시간의 지동평균을 구했기 때문에 앞 11개의 행에는 결측치가 발생함. 그 부분을 제거시켜준다.
    df['daily_rev'] = df['close'].pct_change() + 1

    fng = fngModel(); grad = getGrad()

    # 여기서?

    # RSI를 토대로 코인의 보유여부를 결정한다.
    bt = getBuythreshold(fng, grad)
    st = getSellthreshold(fng)
    df['BUY_THRESHOLD'] = bt
    df['SELL_THRESHOLD'] = st

    df.loc[df['RSI'] < bt, 'signal'] = True
    df.loc[df['RSI'] > st, 'signal'] = False

    # 보유여부
    df.loc[df['signal'].shift(1) == True, 'holding'] = True
    df.loc[df['signal'].shift(1) == False, 'holding'] = False
    df['holding'].ffill(inplace=True)
    df['holding'].fillna(False, inplace=True)


    return df 
 