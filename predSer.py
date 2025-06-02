from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np

app = Flask(__name__)
model = tf.keras.models.load_model(r"C:\Users\karth\Downloads\stress_model.h5")

@app.route("/data", methods=["POST"])
def handle_data():
    data = request.get_json()
    if not data:
        return "Invalid JSON", 400

    sensor1 = float(data["sensor1"])
    sensor2 = float(data["sensor2"])

    input_data = np.array([[sensor1, sensor2]])
    prediction = model.predict(input_data)[0][0]

    print(f"Received: {sensor1}, {sensor2} → Prediction: {prediction}")
    return jsonify({"prediction": float(prediction)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
