import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
import seaborn as sn

# read csv
data_file = 'immo.csv'
df = pd.read_csv(data_file)

# clean data
df = pd.DataFrame(df)
df = df[['Type', 'Price', 'NetHabitableSurface(msq)','street',  'ConstructionYear','BedroomCount', 'locality',  'HeatingType', 'KitchekType', 'FacadeCount','FloodZoneType', 'IsDoubleGlaze']]
columns_to_n = ['Type', 'street',  'locality', 'HeatingType', 'KitchekType', 'FloodZoneType']
columns_to_0 = ['Price',  'BedroomCount']
df[columns_to_n] = df[columns_to_n].replace(np.nan, 'No Value')
df[columns_to_0] = df[columns_to_0].replace(np.nan, 0)
# age of building
list_years = []
for year in df['ConstructionYear']:
    years = 2022 - year
    list_years.append(years)
df = df.assign(ConstructionYear = list_years)

df[['NetHabitableSurface(msq)', 'ConstructionYear']] = df[['NetHabitableSurface(msq)','ConstructionYear']].fillna(df[['NetHabitableSurface(msq)', 'ConstructionYear']].mean())
df['IsDoubleGlaze'] = df['IsDoubleGlaze'].fillna(False)

# encoder
labelencoder = LabelEncoder()
df['Type'] = labelencoder.fit_transform(df['Type'])
df['locality'] = labelencoder.fit_transform(df['locality'])
df['HeatingType'] = labelencoder.fit_transform(df['HeatingType'])
df['KitchekType'] = labelencoder.fit_transform(df['KitchekType'])
df['street'] = labelencoder.fit_transform(df['street'])
df['FloodZoneType'] = labelencoder.fit_transform(df['FloodZoneType'])
df['IsDoubleGlaze'] = labelencoder.fit_transform(df['IsDoubleGlaze'])

# X, y
X = np.array(df[['FloodZoneType','KitchekType','HeatingType','street','BedroomCount','Type', 'ConstructionYear', 'locality', 'NetHabitableSurface(msq)','Price', 'IsDoubleGlaze']])
y = np.array(df['Price'])

# normalize data
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=41, test_size=0.2)
X_train = StandardScaler().fit_transform(X_train)
X_test = StandardScaler().fit_transform(X_test)

# SVM MODEL
from sklearn.svm import SVC

svc_model = SVC()
svc_model.fit(X_train, y_train)
svc_model.score(X_train, y_train)

svg_predict = svc_model.predict(X_test)
svc_model.score(X_test, y_test)

# graph

y_predict = svg_predict.predict(X_test)
cm = confusion_matrix(y_test, y_predict)
plt.figure(figsize=(18,12))
sn.heatmap(cm, annot=True)
