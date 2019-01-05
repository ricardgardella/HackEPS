import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense

def scale_data(dataset, sc=None):
    values = dataset.values
    values = values.astype('float32')
    if sc is None:
        sc = MinMaxScaler(feature_range=(0, 1))
        return sc.fit_transform(values), sc
    return sc.transform(values), sc


def series_to_supervised(data, n_in=1, n_out=1, drop_nan=True):
    n_vars = data.shape[1]
    df = pd.DataFrame(data)
    cols, names = [], []
    # Input sequence
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += ['var{}(t-{})'.format(j + 1, i) for j in range(n_vars)]
    # Output sequence
    cols.append(df.shift(0))
    names += ['var{}(t)'.format(j + 1) for j in range(n_vars)]
    for i in range(1, n_out):
        cols.append(df.shift(-i))
        names += ['var{}(t+{})'.format(j + 1, i) for j in range(n_vars)]

    df = pd.concat(cols, axis=1)
    df.columns = names
    if drop_nan:
        df.dropna(inplace=True)
    return df


def split_dataset(trainset, testset, TIMESTEPS, FEATURES):
    n_obs = TIMESTEPS * FEATURES
    
    values = trainset
    x_train = values[:, :n_obs]
    y_train = values[:, -n_obs]
    
    values = testset
    x_test = values[:, :n_obs]
    y_test = values[:, -n_obs]

    # Reshape into (samples, timesteps, features)
    x_train = x_train.reshape((x_train.shape[0], TIMESTEPS, FEATURES))
    x_test = x_test.reshape((x_test.shape[0], TIMESTEPS, FEATURES))
    print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)
    return x_train, y_train, x_test, y_test


def build_predictor(shapes):
    predictor = Sequential()
    predictor.add(LSTM(units=50, return_sequences=True, input_shape=(shapes[0], shapes[1])))
    predictor.add(LSTM(units=50, return_sequences=True))
    predictor.add(LSTM(units=50))
    predictor.add(Dense(units=1))
    predictor.compile(optimizer='adam', loss='mean_squared_error')
    return predictor


def fit_predictor(predictor, x_train, y_train, x_test, y_test, EPOCHS, BATCH_SIZE):
    history = predictor.fit(x_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE,
                            validation_data=(x_test, y_test), verbose=2, shuffle=False)

    plt.plot(history.history['loss'], label='train')
    plt.plot(history.history['val_loss'], label='test')
    plt.legend()
    plt.show()
    
    return history
