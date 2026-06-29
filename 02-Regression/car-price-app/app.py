import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

with open('model/car_price_model.pkl', 'rb') as f:
    w0, w = pickle.load(f)

with open('model/categories.pkl', 'rb') as f:
    categories = pickle.load(f)

with open('model/base_features.pkl', 'rb') as f:
    base = pickle.load(f)

def prepare_X(df, base, categories):
    df = df.copy()
    features = base.copy()
    df['age'] = 2017 - df['year']
    features.append('age')
    for v in [2, 3, 4]:
        df['num_doors_%s' % v] = (df['number_of_doors'] == v).astype('int')
        features.append('num_doors_%s' % v)
    for c, values in categories.items():
        for v in values:
            df['%s_%s' % (c, v)] = (df[c] == v).astype('int')
            features.append('%s_%s' % (c, v))
    df_num = df[features]
    df_num = df_num.fillna(0)
    return df_num.values

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        car = {
            'make': str(data.get('make', '')).lower().replace(' ', '_'),
            'model': str(data.get('model', '')).lower().replace(' ', '_'),
            'year': int(data.get('year', 2015)),
            'engine_hp': float(data.get('engine_hp', 0)),
            'engine_cylinders': float(data.get('engine_cylinders', 4)),
            'number_of_doors': float(data.get('number_of_doors', 4)),
            'highway_mpg': int(data.get('highway_mpg', 30)),
            'city_mpg': int(data.get('city_mpg', 25)),
            'popularity': int(data.get('popularity', 1000)),
            'engine_fuel_type': str(data.get('engine_fuel_type', '')).lower().replace(' ', '_'),
            'transmission_type': str(data.get('transmission_type', '')).lower().replace(' ', '_'),
            'driven_wheels': str(data.get('driven_wheels', '')).lower().replace(' ', '_'),
            'market_category': str(data.get('market_category', '')).lower().replace(' ', '_'),
            'vehicle_size': str(data.get('vehicle_size', '')).lower().replace(' ', '_'),
            'vehicle_style': str(data.get('vehicle_style', '')).lower().replace(' ', '_'),
        }
        df_input = pd.DataFrame([car])
        X = prepare_X(df_input, base, categories)
        y_pred = w0 + X.dot(w)
        predicted_price = float(np.expm1(y_pred[0]))
        low = round(predicted_price * 0.90, 2)
        mid = round(predicted_price, 2)
        high = round(predicted_price * 1.10, 2)
        return jsonify({'predicted_price': mid, 'price_low': low, 'price_high': high, 'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
