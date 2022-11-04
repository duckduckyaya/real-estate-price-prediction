from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

app = Flask(__name__)



@app.route('/')
def home():
    return "API is working"


@app.route('/predict', methods=['GET','POST'])
def preprocess(features):
    # Load the data
    data = pd.DataFrame(data).from_dict(features, orient='index')
    ohe = OneHotEncoder(handle_unknown='ignore')

    ohe_trans= ohe.fit_transform(np.array(data[['Type', 'locality', 'Province', 'Region', 'HeatingType','IsDoubleGlaze']]))
    ohe_df = pd.DataFrame(ohe_trans, columns=ohe.get_feature_names_out(), index=data.index)

    data = pd.concat([data, ohe_df], axis=1).drop(['Type', 'locality', 'Province', 'Region', 'HeatingType', 'IsDoubleGlaze'], axis=1)

    return data

def predict():
    model = joblib.load('model.pkl')
    if request.method == 'POST':
        # data = request.form.to_dict(features)    #POST
        
        features = request.args.get(features)  #GET
        
        prediction = model.predict(preprocess(features))
        prediction = str(prediction)
        prediction = prediction.strip("[].")  

        price = {
            'price': prediction[0]
        }

        return price
    else:
        request.method == 'GET'
        return "API is working"
    
    


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
