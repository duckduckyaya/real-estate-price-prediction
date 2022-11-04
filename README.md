# Real estate price prediction

1. [Overview](#overview)
2. [Data Acquisition](#data-acquisition)
3. [Data visulization](#data-visulization)
4. [Model Training](#model-training)
5. [Deployment](#deployment)
5. [Libraries](#libraries-used-in-this-project)

---

## Overview

This repo starts from scratch, scraping data from immoweb, cleaning data, data visulization, using model to predict house price, in the end be able to deply the model with render and heroku.

- **Dataset :** immo.csv
- **Description :** data scraped from immoweb.com, write them as csv file

variables in the dataset:

> **1. Type :** type of this property
> **2. Price :** price of property
> **3. BedroomCount :** bedroom number of the property
> **4. Province :** province of the property
> **5. locality :** city of the property
> **6. Region :** region of the property
> **7. NetHabitableSurface :** the property's surface area
> **8. ConstructionYear :** age of the property
> **9. FacadeCount :** the number of facade of th property
> **10. HeatingType :** heating type of the property
> **11. IsDoubleGlaze :** is the property has doble glass

## Data acquisition

Using `beautifulsoup` `requests` to scrape house information from www.immoweb.com, the imformation only contains **house** and **apartment**. The informations has already saved as **csv** file in the folder of ==data-acquisition==

Using `pandas` `numpy` to clean the data, drop duplicate and nan value column, make the data more readable. using `regex` to remove extra sign (brackets and back slash etc...)

![image info](/assets/data-clearn.jpg)

## Data analysis

Using `pandas` `matplotlib` to analyse real estate information scaped from www.immoweb.com. get mean price of each property with range of price, replace them, change the column name to more human readable.

Using `matplotlib` to visialize the analysis using ==bar plot== and ==bar chart== according to the dataset
analysis **Belgium average house price per province compare to number of house per province**

### dataframe 1

![image info](/assets/chart.jpg)

### plot 1

![image info](/assets/bar-plot.jpg)

### dataframe 2

![image info](/assets/dataset2.jpg)
![image info](/assets/plot2.jpg)

## Model Training

In the
Training the model to be able to predict the property price. For this project, I used `Linear regression`, `Random forest` to train the model, on the `preprocessing` part, i used OneHotEncoder to convert categories to binary, and used pipeline as well

```python
num_feature = ['BedroomCount', 'NetHabitableSurface']
cate_feature = ['Type', 'Province', 'locality', 'Region', 'FloodZoneType', 'HeatingType', 'KitchekType']

num_trans = Pipeline([('scaler', StandardScaler())])
cate_trans = Pipeline([('ohe', OneHotEncoder(handle_unknown='ignore', sparse=False))])

preprocessor = ColumnTransformer([('num_transformer', num_trans, num_feature),
                                ('cate_transformer', cate_trans, cate_feature)])
```

then `fit_transform` the train and test set

```python
trans_train = preprocessor.fit_transform(X_train)
trans_test = preprocessor.fit_transform(X_test)
```

In the end be able to get the model trained with `RandomForestRegressor`

save it as `model.pkl` file in the  ==deployment folder==

## Deployment

In this folder, create `docker` container to store the project, having `preprocess function` to preprocess the data, so that the model can predict price

Creat API working from `app.py` file with **flask Api**, save the model with working API in the docker

`render` the prediction model by **render.com**, so that the prediction model can be on dynamic web

## Libraries used in this project
>
> - pandas
> - numpy
> - flask
> - joblib
> - sklearn
> - json
> - matplotlib
> - seaborn
> - beautifulSoup
> - requests
> - regex
> - csv
