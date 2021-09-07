import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import read_csv
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.layers.core import Dense, Activation, Dropout
import time 

look_back = 5      # 輸入股價天數
neurons = 200      # 記憶神經元個數

# 前 look_back 天股價為 input
# 第 look_back 天股價為 label
def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return np.array(dataX), np.array(dataY)

# 使用固定亂數種子, 使每次執行結果一樣
np.random.seed(5)

# 載入股票
input_file="stock2317.csv"
df = read_csv(input_file, header=None, index_col=None, delimiter=',')
all_y = df[5].values                           # 取第五欄鴻海股票收盤價


dataset=all_y.reshape(-1, 1)                   # 股票價格數值正規化至 [-1, 1]
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)        # 股票價格數值正規化至 [0, 1]

train_size = int(len(dataset) * 0.5)           # 前50%為訓練資料集, 2517 筆
test_size = len(dataset) - train_size          # 後50%為測試資料集, 2518 筆
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]

# 重塑陣列形狀 X=1~t and Y=t+1
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)

# 重塑陣列形狀 [samples, time steps, features]
trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

# 訓練 LSTM 網路 
# optimizer=adam
# 100 neurons
# dropout 0.1
# epochs 10
model = Sequential()
model.add(LSTM(neurons, input_shape=(1, look_back)))
model.add(Dropout(0.1))
model.add(Dense(1))
model.compile(loss='mse', optimizer='adam')
model.fit(trainX, trainY, epochs=10, batch_size=look_back, verbose=1)

# 股價預測
trainPredict = model.predict(trainX)
testPredict = model.predict(testX)

# 反正規化, 還原股價
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])

# 計算根均方誤差 RMSE (root mean squared error)
trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
print('Test Score: %.2f RMSE' % (testScore))

# 平移訓練資料集預測結果以便繪圖
trainPredictPlot = np.empty_like(dataset)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict

# 平移測試資料集預測結果以便繪圖
testPredictPlot = np.empty_like(dataset)
testPredictPlot[:, :] = np.nan
testPredictPlot[len(trainPredict)+(look_back*2)+1:len(dataset)-1, :] = testPredict

# 繪圖
plt.plot(scaler.inverse_transform(dataset))  # 真實股價
plt.plot(trainPredictPlot)                   # 預測股價
print('testPrices:')
testPrices=scaler.inverse_transform(dataset[test_size+look_back:])

print('testPredictions:')
print(testPredict)

# export prediction and actual prices
df = pd.DataFrame(data={"prediction": np.around(list(testPredict.reshape(-1)), decimals=2), "test_price": np.around(list(testPrices.reshape(-1)), decimals=2)})
df.to_csv("lstm_result.csv", sep=';', index=None)

# 繪製測試資料集預測結果:  in test data=red line, actual price=blue line
plt.plot(testPredictPlot)
plt.show()


