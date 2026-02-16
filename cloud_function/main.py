import joblib
import json

# Load model once (cold start)
model = joblib.load("model.pkl")

def predict(request):
    """
    HTTP Cloud Function for iris prediction
    """
    try:
        data = request.get_json(silent=True)

        features = [[
            data["sepal_length"],
            data["sepal_width"],
            data["petal_length"],
            data["petal_width"]
        ]]

        prediction = model.predict(features)[0]

        return {
            "prediction": prediction,
            "model_loaded": True
        }

    except Exception as e:
        return {
            "error": str(e)
        }, 400
