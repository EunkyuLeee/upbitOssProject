import pyupbit
import matplotlib.pyplot as plt

 

def getGrad():
    '''
    시작점 < 좀점 -> return 1
    시작점 > 종점 -> reurn -1
    else -> return 0
    '''
    dataset = pyupbit.get_ohlcv('KRW-BTC', interval="minute60")

    s = dataset['close'].iloc[0]
    e = dataset['close'].iloc[-1]
    if s < e :
        return 1
    elif s > e:
        return -1
    
    return 0
