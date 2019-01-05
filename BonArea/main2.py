import pandas as pd
from datetime import datetime, timedelta

DATASET_FILE = 'dades_train_P2.csv'

df = pd.read_csv(DATASET_FILE)

# Drop trash columns
df = df.drop(['Provincia', 'Linia', 'Pes_mig_G', 'Preu_Total', 'Mesura'], axis=1)


# Date columns
df.Dia_Comanda = pd.to_datetime(df.Dia_Comanda, format='%Y-%m-%d')
df.Dia_Servei = pd.to_datetime(df.Dia_Servei, format='%Y-%m-%d')

min_date = df.Dia_Comanda.min()
df = df.loc[df['Dia_Comanda'] > (datetime.now() - timedelta(days=2*365))]
df['Setmana'] = df['Dia_Comanda'].map(lambda e: (e.year - min_date.year) * 54 + e.isocalendar()[1]) # TODO: min 51

df = df.drop(['Dia_Comanda', 'Dia_Servei'], axis=1)

# Combine columns
df.Unitats_Demanades = (df.Unitats_Demanades - df.Unitats_Servides) * df.UxC
df = df.rename(columns={'Unitats_Demanades': 'Unitats_Perdudes'})
df = df.drop(['Unitats_Servides', 'UxC'], axis=1)

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

