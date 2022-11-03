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
def preprocess(data):
    # Load the data
    data = pd.DataFrame(data)
    ohe = OneHotEncoder(handle_unknown='ignore')

    ohe_df = pd.DataFrame(ohe.fit_transform(np.array(data[['Type', 'locality', 'Province', 'Region', 'HeatingType','IsDoubleGlaze']])))

    data = pd.concat([data, ohe_df], axis=1).drop(['Type', 'locality', 'Province', 'Region', 'HeatingType', 'IsDoubleGlaze'], axis=1)

    return jsonify(data)

def predict():
    model = joblib.load('model.pkl')
    if request.method == 'POST':
        data = request.get_json()
        prediction = model.predict(preprocess(data))

        price = {
            'price': prediction[0]
        }

        return jsonify(price)
    else:
        request.method == 'GET'
        return "API is working"
    
    


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
