import json
import boto3
import pandas as pd
import joblib
from io import BytesIO

# Configurazioni fisse
BUCKET_MODEL = "ssdc--bucket"
MODEL_KEY = "model/random_forest_model.pkl"
ENCODERS_KEY = "preprocessed/label_encoders.pkl"
SCALER_KEY = "preprocessed/scaler.pkl"

cat_cols = ["workclass", "education", "marital_status", "occupation",
            "relationship", "race", "sex", "native_country"]
num_cols = ["age", "fnlwgt", "education_num", "capital_gain", "capital_loss", "hours_per_week"]

s3 = boto3.client("s3")

def load_object_from_s3(bucket, key):
    obj = s3.get_object(Bucket=bucket, Key=key)
    return obj["Body"].read()

def load_model_and_processors():
    model_bytes = load_object_from_s3(BUCKET_MODEL, MODEL_KEY)
    model = joblib.load(BytesIO(model_bytes))

    encoders_bytes = load_object_from_s3(BUCKET_MODEL, ENCODERS_KEY)
    label_encoders = joblib.load(BytesIO(encoders_bytes))

    scaler_bytes = load_object_from_s3(BUCKET_MODEL, SCALER_KEY)
    scaler = joblib.load(BytesIO(scaler_bytes))

    return model, label_encoders, scaler

model, label_encoders, scaler = load_model_and_processors()

def preprocess_input(data_dict):
    df = pd.DataFrame([data_dict])

    for col in cat_cols:
        le = label_encoders[col]
        df[col] = le.transform([df[col].values[0]])

    df[num_cols] = scaler.transform(df[num_cols])

    return df

def predict_income(data_dict):
    X = preprocess_input(data_dict)
    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0][1]
    return {
        "prediction": int(prediction),
        "probability_of_>50K": round(probability, 3)
    }


def cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }

def lambda_handler(event, context):
    # Ottieni il metodo HTTP
    method = event.get("requestContext", {}).get("http", {}).get("method", "")

    # Rispondi alla preflight CORS (OPTIONS)
    if method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": cors_headers(),
            "body": ""
        }

    # Gestione POST (o altri metodi)
    try:
        body = event.get("body")
        if not body:
            return {
                "statusCode": 400,
                "headers": cors_headers(),
                "body": json.dumps({"error": "Missing request body"})
            }

        data = json.loads(body)

        missing_fields = [col for col in cat_cols + num_cols if col not in data]
        if missing_fields:
            return {
                "statusCode": 400,
                "headers": cors_headers(),
                "body": json.dumps({"error": f"Missing fields: {missing_fields}"})
            }

        result = predict_income(data)

        return {
            "statusCode": 200,
            "headers": {**cors_headers(), "Content-Type": "application/json"},
            "body": json.dumps(result)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": cors_headers(),
            "body": json.dumps({"error": str(e)})
        }
