import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def preprocess(data):
    # Load the data
    data = pd.DataFrame(data).from_dict(data, orient='index')
    ohe = OneHotEncoder(handle_unknown='ignore')

    ohe_trans= ohe.fit_transform(np.array(data[['Type', 'locality', 'Province', 'Region', 'HeatingType','IsDoubleGlaze']]))
    ohe_df = pd.DataFrame(ohe_trans, columns=ohe.get_feature_names_out(), index=data.index)

    data = pd.concat([data, ohe_df], axis=1).drop(['Type', 'locality', 'Province', 'Region', 'HeatingType', 'IsDoubleGlaze'], axis=1)

    return data
