import numpy as np
import pandas as pd
from  sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
import json


# data cleaning

data_file = 'immo.csv'
df = pd.read_csv(data_file)

# drop column has nan missing values for more than 60%
df = pd.DataFrame(df)
df = df.drop(['ID','PostCode', 'Sub type', 'Floor', 'IsIsolated', 'HasSeaView', 'TotalRoomCount', 'HasAttic',  'HasDiningRoom',    'GardenArea', 'LivingRoomArea', 'NetHabitableSurface(msq)', 'SchoolDistance', 'ShopDistance', 'TransportDistance', 'BuildingCondition','RegionCode','street'], axis=1)

# age of building
list_years = []
for year in df['ConstructionYear']:
    years = 2022 - year
    list_years.append(years)
df = df.assign(ConstructionYear = list_years)

# replace & drop nan values
df[['NetHabitableSurface', 'ConstructionYear']] = df[['NetHabitableSurface','ConstructionYear']].fillna(df[['NetHabitableSurface', 'ConstructionYear']].mean())
columns_to_n = ['Type', 'locality', 'KitchekType']
df[columns_to_n] = df[columns_to_n].replace(np.nan, 'No Value')
df = df.drop_duplicates()
df = df.dropna(subset=['BedroomCount', 'Price', 'Province'])

# replace nan value in heating type with most frequent value
heating_type = df['HeatingType'].mode()[0]
facade_count = df['FacadeCount'].mode()[0]
flood_zone_type = df['FloodZoneType'].mode()[0]

df = df.fillna({'HasLift': False, 'HasBalcony': False,  'HasGarden': False, 'HasBasement': False,  'IsDoubleGlaze': False, 'HeatingType':heating_type, 'FacadeCount': facade_count, 'FloodZoneType':flood_zone_type})

#turn data type to int
df['NetHabitableSurface'] = df['NetHabitableSurface'].astype('int')
df['Price'] = df['Price'].astype('int')
df['BedroomCount'] = df['BedroomCount'].astype('int')
df['ConstructionYear'] = df['ConstructionYear'].astype('int')
df['FacadeCount'] = df['FacadeCount'].astype('int')

df = df.dropna(subset=['Price', 'NetHabitableSurface', 'BedroomCount', 'Province', 'Region'])

df.columns


# pipeline normorlize ohe
num_feature = ['BedroomCount', 'NetHabitableSurface']
cate_feature = ['Type', 'Province', 'locality', 'Region', 'FloodZoneType', 'HeatingType', 'KitchekType']

num_trans = Pipeline([('scaler', StandardScaler())])
cate_trans = Pipeline([('ohe', OneHotEncoder(handle_unknown='ignore', sparse=False))])

preprocessor = ColumnTransformer([('num_transformer', num_trans, num_feature),
                                ('cate_transformer', cate_trans, cate_feature)])


# split data
X = df.drop('Price', axis=1)
y = df['Price']

X_train, X_test, y_train, y_test = train_test_split(X,y,random_state=0,  test_size=0.2)
X.columns


trans_train = preprocessor.fit_transform(X_train)
trans_test = preprocessor.fit_transform(X_test)

# random forest
rf = RandomForestRegressor()

rf.fit(trans_train, y_train)
y_predict = rf.predict(trans_test)

#
model = joblib.load('rt_model.pkl')


predictions = model.predict(trans_test)
predictions

