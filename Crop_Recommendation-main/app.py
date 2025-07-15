from flask import Flask,request,render_template
import numpy as np

import pickle

model = pickle.load(open('F:/Machine Learning Projects/Crop_Recommendation-main/model.pkl','rb'))
sc = pickle.load(open('F:/Machine Learning Projects/Crop_Recommendation-main/standscaler.pkl','rb'))
mx = pickle.load(open('F:/Machine Learning Projects/Crop_Recommendation-main/minmaxscaler.pkl','rb'))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/predict",methods=['POST'])
def predict():

    try:
        N = float(request.form['Nitrogen'])
        P = float(request.form['Phosporus'])
        K = float(request.form['Potassium'])
        temp = float(request.form['Temperature'])
        humidity = float(request.form['Humidity'])
        ph = float(request.form['pH'])
        rainfall = float(request.form['Rainfall'])
    except (ValueError, KeyError):
        return render_template('index.html', result="Invalid input. Please enter valid numbers for all fields.")

    feature_list = [N, P, K, temp, humidity, ph, rainfall]
    single_pred = np.array(feature_list, dtype=float).reshape(1, -1)

    try:
        mx_features = mx.transform(single_pred)
        sc_mx_features = sc.transform(mx_features)
        prediction = model.predict(sc_mx_features)
    except Exception as e:
        return render_template('index.html', result=f"Prediction error: {str(e)}")

    # If model returns string label
    if isinstance(prediction[0], str):
        crop = prediction[0]
        result = f"{crop} is the best crop to be cultivated right there"
    else:
        crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
                     8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
                     14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
                     19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"}
        if prediction[0] in crop_dict:
            crop = crop_dict[prediction[0]]
            result = f"{crop} is the best crop to be cultivated right there"
        else:
            result = "Sorry, we could not determine the best crop to be cultivated with the provided data."
    return render_template('index.html', result=result)


if __name__ == "__main__":
    app.run(debug=True)