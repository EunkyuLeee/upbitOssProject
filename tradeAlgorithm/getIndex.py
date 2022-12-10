
import pyupbit
import matplotlib.pyplot as plt

dataset = pyupbit.get_ohlcv('KRW-BTC', interval="minute60")


def getGrad():
    '''
    시작점 < 좀점 -> return 1
    시작점 > 종점 -> reurn -1
    else -> return 0
    '''
    s = dataset['close'].iloc[0]
    e = dataset['close'].iloc[-1]
    if s < e :
        return 1
    elif s > e:
        return -1
    else:
        return 0

def getDelta():
    delta = 0
    prev = -1
    for d in dataset['close']:
        if prev == -1:
            prev = d
        else:
            # print(d-prev)
            delta += (d - prev)
            prev = d 
    return delta / 10000

print('======start=======')
print(dataset)
print(dataset['close'])
print('=-=====-==')
print(getGrad())
print('-----')
print(getDelta())

plt.plot(dataset['close'])
plt.show()