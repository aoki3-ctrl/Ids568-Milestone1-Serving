from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Milestone 2 ML Service Running"})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy"
    })

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        values = list(data.values())
        total = np.sum(values)

        prediction = "positive" if total > 2 else "negative"

        return jsonify({
            "prediction": prediction
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
