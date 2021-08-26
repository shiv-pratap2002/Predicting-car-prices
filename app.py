from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
# from sklearn.preprocessing import StandardScaler
# import os

# scores = {} # scores is an empty dict already

# if os.path.getsize(target) > 0:      
#     with open(target, "rb") as f:
#         unpickler = pickle.Unpickler(f)
#         # if file is not empty scores will be equal
#         # to the value unpickled
#         scores = unpickler.load()
app = Flask(__name__,template_folder='templates')
model = pickle.load(open('RandomForest.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('temp.html')


# standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Age = int(request.form['Year'])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        # Kms_Driven2=np.log(Kms_Driven)
        Owner=int(request.form['Owner'])
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
        elif(Fuel_Type_Petrol=='Diesel'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
        Age=2020-Age
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0	
        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
        prediction=model.predict([[Present_Price,Kms_Driven,Owner, Age, Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual, Transmission_Mannual]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('temp.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('temp.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('temp.html')

if __name__=="__main__":
    app.run(debug=True)