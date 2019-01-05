import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

DATASET_TRAIN_PATH = 'dades_train_P1.csv'
DATASET_TEST_PATH = 'dades_test.csv'

TIMESTEPS = 14
EPOCHS = 50
BATCH_SIZE = 32


def preprocess_dataset(path):
    dataset = pd.read_csv(path, date_parser=lambda d: datetime.strptime(d, '%Y %m %d %H'))
    plt.matshow(dataset.corr())
    plt.figure()
    for group in range(0, 2):
        plt.subplot(2, 1, group + 1)
        plt.plot(dataset.values[:, group])
        plt.title(dataset.columns[group], y=0.5, loc='right')
    plt.show()
    return dataset


def scale_data(dataset, sc=None):
    if sc is None:
        sc = MinMaxScaler(feature_range=(0, 1))
    values = dataset.values
    values = values.astype('float32')
    return sc.fit_transform(values), sc


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


def build_predictor(shapes):
    predictor = Sequential()
    predictor.add(LSTM(units=50, return_sequences=True, input_shape=(shapes[0], shapes[1])))
    predictor.add(LSTM(units=50, return_sequences=True))
    predictor.add(LSTM(units=50))
    predictor.add(Dense(units=1))
    predictor.compile(optimizer='adam', loss='mean_squared_error')
    return predictor


def fit_predictor(predictor, x_train, y_train, x_test, y_test):
    history = predictor.fit(x_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE,
                            validation_data=(x_test, y_test), verbose=2, shuffle=False)

    plt.plot(history.history['loss'], label='train')
    plt.plot(history.history['val_loss'], label='test')
    plt.legend()
    plt.show()


df_train = preprocess_dataset(DATASET_TRAIN_PATH)
df_test = preprocess_dataset(DATASET_TEST_PATH)

df_train, sc = scale_data(df_train)
df_test = scale_data(df_test)

df_train = series_to_supervised(df_train, TIMESTEPS, 1)
