from flask import Flask, render_template, request
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model  # type: ignore

app = Flask(__name__)

model = load_model('models/ann_model.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('loan.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        no_of_dependents = int(request.form['no_of_dependents'])
        income_annum = float(request.form['income_annum'])
        loan_amount = float(request.form['loan_amount'])
        loan_term = int(request.form['loan_term'])
        cibil_score = int(request.form['cibil_score'])

        residential_assets_value = float(request.form['residential_assets_value'])
        commercial_assets_value = float(request.form['commercial_assets_value'])
        luxury_assets_value = float(request.form['luxury_assets_value'])
        bank_asset_value = float(request.form['bank_asset_value'])

        education_not_graduate = 1 if request.form['education_NotGraduate'] == 'Yes' else 0
        self_employed_yes = 1 if request.form['self_employed_Yes'] == 'Yes' else 0

        features = np.array([
            no_of_dependents,
            income_annum,
            loan_amount,
            loan_term,
            cibil_score,
            residential_assets_value,
            commercial_assets_value,
            luxury_assets_value,
            bank_asset_value,
            education_not_graduate,
            self_employed_yes
        ]).reshape(1, -1)

        prediction = model.predict(features)
        prediction = (prediction > 0.5).astype(int)[0][0]

        prediction_text = "APPROVED" if prediction == 1 else "REJECTED"
        result_class = "approved" if prediction == 1 else "rejected"

        # Render the output.html with input data and prediction result
        return render_template('output.html', 
                               result=prediction_text,
                               result_class=result_class,
                               no_of_dependents=no_of_dependents,
                               income_annum=income_annum,
                               loan_amount=loan_amount,
                               loan_term=loan_term,
                               cibil_score=cibil_score,
                               residential_assets_value=residential_assets_value,
                               commercial_assets_value=commercial_assets_value,
                               luxury_assets_value=luxury_assets_value,
                               bank_asset_value=bank_asset_value,
                               education_not_graduate='Yes' if education_not_graduate else 'No',
                               self_employed='Yes' if self_employed_yes else 'No')

    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
