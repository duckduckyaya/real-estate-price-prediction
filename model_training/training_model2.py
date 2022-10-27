import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

# read csv
data_file = 'immo.csv'
df = pd.read_csv(data_file)

# clean data
df = pd.DataFrame(df)
df = df[['Type', 'Price', 'NetHabitableSurface(msq)', 'street', 'ConstructionYear', 'BedroomCount', 'locality',
         'HeatingType', 'KitchekType']]
columns_to_n = ['Type', 'street', 'locality', 'HeatingType', 'KitchekType']
columns_to_0 = ['Price', 'NetHabitableSurface(msq)', 'ConstructionYear', 'BedroomCount']
df[columns_to_n] = df[columns_to_n].replace(np.nan, 'None')
df[columns_to_0] = df[columns_to_0].replace(np.nan, 0)

# encoder
labelencoder = LabelEncoder()
df['Type'] = labelencoder.fit_transform(df['Type'])
df['locality'] = labelencoder.fit_transform(df['locality'])
df['HeatingType'] = labelencoder.fit_transform(df['HeatingType'])
df['KitchekType'] = labelencoder.fit_transform(df['KitchekType'])
df['street'] = labelencoder.fit_transform(df['street'])

# X, y
X = np.array(df[['KitchekType', 'HeatingType', 'street', 'BedroomCount', 'Type', 'ConstructionYear', 'locality',
                 'NetHabitableSurface(msq)']])
y = np.array(df['Price'])

# normalize data
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=41, test_size=0.2)
X_train = StandardScaler().fit_transform(X_train)
X_test = StandardScaler().fit_transform(X_test)

# KNN MODEL
from sklearn.neighbors import KNeighborsClassifier

knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(X_train, y_train)
knn_model.score(X_train, y_train)

knn_predict = knn_model.predict(X_test)
knn_model.score(X_test, y_test)

# LINEAR REGRESSION
regression = LinearRegression()
regression.fit(X_train, y_train)
regression.score(X_train, y_train)

linear_predict = regression.predict(X_test)
regression.score(X_test, y_test)

# RANDOM FOREST MODEL
from sklearn.ensemble import RandomForestClassifier

rt_model = RandomForestClassifier()
rt_model.fit(X_train, y_train)
rt_model.score(X_train, y_train)

rt_model.predict(X_test)
rt_model.score(X_test, y_test)

# SVM MODEL
from sklearn.svm import SVC

svc_model = SVC()
svc_model.fit(X_train, y_train)
svc_model.score(X_train, y_train)

svg_predict = svc_model.predict(X_test)
svc_model.score(X_test, y_test)
