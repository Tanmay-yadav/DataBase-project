from flask import Flask, render_template, request
import joblib
import numpy as np
import warnings
from pricedata import create_table, insert_prediction

warnings.filterwarnings('ignore')

# Initialize the SQLite database and create the table
create_table()

model = joblib.load('oldbikepricepredction/models/linearRegression.lb')
app = Flask(__name__)

@app.route('/')
def Home():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        kms_driven = int(request.form['Kms_Driven'])
        owner = int(request.form['owner'])
        age = int(request.form['age'])
        power = int(request.form['power'])
        brand = request.form['brand_name']

        brand_mapping = {
            'Royal Enfield': 1, 'KTM': 2, 'Bajaj': 3, 'Harley': 4,
            'Yamaha': 5, 'Honda': 6, 'Suzuki': 7, 'TVS': 8,
            'Kawasaki': 9, 'Hyosung': 10, 'Benelli': 11, 'Mahindra': 12,
            'Triumph': 13, 'Ducati': 14, 'BMW': 15
        }

        brand_mapped = brand_mapping.get(brand, 0)  # Default to 0 if brand not found

        prediction = model.predict([[kms_driven, owner, age, power, brand_mapped]])
        output = str(prediction[0].round(2))  # Round to 2 decimal places

        # Prepare data for insertion into the database
        data = {
            'kms_driven': kms_driven,
            'owner': owner,
            'age': age,
            'power': power,
            'brand': brand,
            'prediction': output
        }

        # Insert the data into the database
        insert_prediction(data)

        return render_template('output.html', 
                               prediction=output,
                               kms_driven=kms_driven,
                               owner=owner,
                               age=age,
                               power=power,
                               brand=brand)
    return render_template('predict.html')

if __name__ == "__main__":
    app.run(debug=True)
