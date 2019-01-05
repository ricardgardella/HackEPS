import pandas as pd
<<<<<<< Updated upstream
from datetime import datetime
from helpers import scale_data, series_to_supervised, split_dataset, build_predictor, fit_predictor
=======
from datetime import datetime, timedelta
from helpers import scale_data, series_to_supervised, merge
>>>>>>> Stashed changes

TRAINSET_FILE = 'dades_train_P1.csv'
TESTSET_FILE = 'dades_test.csv'

PAST_TIMESTEPS = 12
FUTURE_TIMESTEPS = 3
FEATURES = 12
EPOCHS = 10
BATCH_SIZE = 100


df_train = pd.read_csv(TRAINSET_FILE,
                       parse_dates=['Dia_Comanda'], index_col=4,
                       date_parser=lambda d: datetime.strptime(d, '%Y-%m-%d'))

df_test = pd.read_csv(TESTSET_FILE,
                      parse_dates=['Dia_Comanda'], index_col=4,
                      date_parser=lambda d: datetime.strptime(d, '%Y-%m-%d'))

# Drop not useful columns
df_train = df_train.drop(['Provincia', 'Linia', 'Pes_mig_G', 'Preu_Total', 'Mesura'], axis=1)
df_test = df_test.drop(['Provincia', 'Linia', 'Pes_mig_G', 'Preu_Total', 'Mesura'], axis=1)

# Date columns
min_date = df['Dia_Comanda'].min()
# df = df.loc[df['Dia_Comanda'] > (datetime.now() - timedelta(days=2*365))]
<<<<<<< Updated upstream
# df['Setmana'] = df['Dia_Comanda'].map(lambda e: (e.year - min_date.year) * 54 + e.isocalendar()[1]) # TODO: min 51

df_train = df_train.drop(['Dia_Servei'], axis=1)
df_test = df_test.drop(['Dia_Servei'], axis=1)

# Combine columns
df_train.Unitats_Demanades = (df_train.Unitats_Demanades - df_train.Unitats_Servides) * df_train.UxC
df_train = df_train.rename(columns={'Unitats_Demanades': 'Unitats_Perdudes'})
df_train = df_train.drop(['Unitats_Servides', 'UxC'], axis=1)
df_test.Unitats_Demanades = (df_test.Unitats_Demanades - df_test.Unitats_Servides) * df_test.UxC
df_test = df_test.rename(columns={'Unitats_Demanades': 'Unitats_Perdudes'})
df_test = df_test.drop(['Unitats_Servides', 'UxC'], axis=1)


=======
df['week'] = map(lambda e: (e.year - min_date.year) * 54 + e.isocalendar()[1], df.index.values) # TODO: min 51
df = df[df['week'] > df['week'].max() - PAST_TIMESTEPS]
df['week'] = map(lambda x: df['week'].max()-x)
df = df.group_by('Client').apply(lambda x: merge(x, PAST_TIMESTEPS))
print(df)
>>>>>>> Stashed changes
#####

scaled = scale_data(df_train)
trainset = scaled
# series_to_supervised(scaled, PAST_TIMESTEPS, FUTURE_TIMESTEPS)

scaled = scale_data(df_test)
testset = scaled
# series_to_supervised(scaled, PAST_TIMESTEPS, FUTURE_TIMESTEPS)

x_train, y_train, x_test, y_test = split_dataset(trainset, testset, PAST_TIMESTEPS, FUTURE_TIMESTEPS)
predictor = build_predictor((x_train.shape[1], x_train.shape[2]))
fit_predictor(predictor, x_train, y_train, x_test, y_test, EPOCHS, BATCH_SIZE)

#####


# TODO: OneHotEncoding
from sklearn.preprocessing import LabelEncoder
df.Client = LabelEncoder().fit_transform(df.Client)
df.Poblacio = LabelEncoder().fit_transform(df.Poblacio)
df.Tipus_Client = LabelEncoder().fit_transform(df.Tipus_Client)
df.Article = LabelEncoder().fit_transform(df.Article)
df.Congelat = LabelEncoder().fit_transform(df.Congelat)
df.Lloc_Descarrega = LabelEncoder().fit_transform(df.Lloc_Descarrega)
df.Bonarea = LabelEncoder().fit_transform(df.Bonarea)

# Split Dependent/Independent vars
X = df.iloc[:, 0:-2].values
y = df.iloc[:, -2].values

# Split dataset
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

from keras.models import Sequential
from keras.layers import Dense
classifier = Sequential()    
classifier.add(Dense(12, kernel_initializer='random_uniform', activation='relu'))    
classifier.add(Dense(1, kernel_initializer='random_uniform', activation='sigmoid'))
classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Evaluation
classifier.fit(X_train, y_train, batch_size=100, epochs=10)
prediction = classifier.predict(X_test)
y_pred = prediction > 0.5

# Confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
accuracy = (cm[0, 0] + cm[1, 1]) / sum(sum(cm))
