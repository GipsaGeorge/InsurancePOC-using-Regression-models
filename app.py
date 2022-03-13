#Importing the required libraries
from flask import Flask, request,render_template

#pickle for loading the insurance model
import pickle

#numpy for mathematical operations
import numpy as np

app = Flask(__name__)

#Loading the model
model = pickle.load(open('insurance.pkl', 'rb'))

#defining the main index route
@app.route('/')
def home():
    return render_template('InsuranceModel.html')

# prediction function
def ChargePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1,5)
    loaded_model = pickle.load(open("insurance.pkl", "rb"))
    result = loaded_model.predict(to_predict)
    print(result[0])
    return result[0]


#this route will be called when the predict button is clicked
@app.route('/predict', methods = ['POST','GET'])
def predict():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        if to_predict_list[1] == 'Male':
            to_predict_list[1] = 1
        else:
            to_predict_list[1] = 0
        if to_predict_list[4] == 'yes':
            to_predict_list[4] = 1
        else:
            to_predict_list[4] = 0

        to_predict_list = list(map(float, to_predict_list))
        result = round(ChargePredictor(to_predict_list), 2)
        return render_template("result.html", prediction=result)

# Main function
if __name__ == "__main__":
    app.run(debug=True)
    app.config['TEMPLATES_AUTO_RELOADED'] = True