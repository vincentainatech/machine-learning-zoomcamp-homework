# Car Price Prediction App

## Project Goal
Help users estimate the MSRP of their car before selling it.

## Tech Stack
- Backend: Python + Flask
- Frontend: Vanilla HTML, CSS, JavaScript (no frameworks)
- Model: Custom linear regression (w0 + X.dot(w))

## Project Structure
car-price-app/
├── app.py              → Flask API server
├── CLAUDE.md           → This file
├── requirements.txt    → Python dependencies
├── model/
│   ├── car_price_model.pkl  → w0 (bias) and w (weights)
│   ├── categories.pkl       → categorical variable encodings
│   ├── base_features.pkl    → base numeric feature list
│   └── prepare_x.py         → feature engineering function
├── templates/
│   └── index.html      → Main page with car input form
└── static/
    ├── style.css        → Styling
    └── app.js           → Form submission and result display

## Model Details
- Type: Custom Linear Regression with regularization (r=0.001)
- Target: np.log1p(MSRP) — must use np.expm1() to get real price
- Trained on: car price dataset with ~11,000 cars

## Model Inputs (form fields)
| Field              | Type    | Example            |
|--------------------|---------|--------------------|
| make               | string  | toyota, bmw        |
| model              | string  | corolla            |
| year               | integer | 2015               |
| engine_hp          | float   | 150.0              |
| engine_cylinders   | float   | 4.0                |
| number_of_doors    | float   | 4.0                |
| highway_mpg        | integer | 30                 |
| city_mpg           | integer | 25                 |
| popularity         | integer | 1000               |
| engine_fuel_type   | string  | regular_unleaded   |
| transmission_type  | string  | automatic          |
| driven_wheels      | string  | front_wheel_drive  |
| market_category    | string  | crossover          |
| vehicle_size       | string  | compact            |
| vehicle_style      | string  | sedan              |

## How Prediction Works
1. Take form inputs as a Python dictionary
2. Convert to a single-row pandas DataFrame
3. Run prepare_X(df, base, categories) to get feature vector
4. Predict: y_pred = w0 + X.dot(w)
5. Convert back to real price: price = np.expm1(y_pred[0])
6. Return price as JSON to the frontend

## API Endpoint
POST /predict
- Input: JSON with car fields above
- Output: { "predicted_price": 23456.78 }

## Design
- Clean, professional, trustworthy feel
- Dark navy and white color scheme
- Two column layout: form on left, results on right
- Show predicted price prominently
- Mobile friendly
