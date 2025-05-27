import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import boto3

def lambda_handler(event, context):
    s3_client = boto3.client("s3")

    bucket_name = "ssdc--bucket"

    # Percorso del file preprocessato in S3 (passato da evento oppure default)
    s3_key = event.get("s3_key", "preprocessed/adult_clean_label_encoded.csv")

    # Percorso locale temporaneo
    local_path = "/tmp/adult_clean_label_encoded.csv"

    # Scarica dataset preprocessato da S3
    s3_client.download_file(bucket_name, s3_key, local_path)

    # Carica dataset
    df = pd.read_csv(local_path)

    # Separazione feature e target
    X = df.drop("income", axis=1)
    y = df["income"]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Addestramento modello
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Salvataggio modello localmente
    model_path = "/tmp/random_forest_model.pkl"
    joblib.dump(model, model_path)

    print("Modello salvato in /tmp")

    # Upload modello su S3 nella cartella model/
    model_s3_key = "model/random_forest_model.pkl"
    s3_client.upload_file(model_path, bucket_name, model_s3_key)

    print(f"Modello caricato su S3: s3://{bucket_name}/{model_s3_key}")

    return {
        'statusCode': 200,
        'body': 'Model trained and saved to S3 successfully.'
    }
