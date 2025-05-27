import joblib
import pandas as pd
import boto3
import json
from sklearn.preprocessing import LabelEncoder, StandardScaler

def lambda_handler(event, context):
    s3 = boto3.client("s3")

    bucket_name = "ssdc--bucket"
    # Qui prendi il key del file caricato che ha triggerato la lambda
    dataset_key = event['Records'][0]['s3']['object']['key']
    local_dataset_path = "/tmp/adult.data"

    try:
        s3.download_file(bucket_name, dataset_key, local_dataset_path)
        print(f"Scaricato dataset da s3://{bucket_name}/{dataset_key}")
    except Exception as e:
        print("Errore nel download:", str(e))
        return {
            'statusCode': 500,
            'body': f"Errore nel download da S3: {str(e)}"
        }

    df = pd.read_csv(local_dataset_path, header=None, na_values="?", skipinitialspace=True)
    df.columns = [
        "age", "workclass", "fnlwgt", "education", "education_num",
        "marital_status", "occupation", "relationship", "race", "sex",
        "capital_gain", "capital_loss", "hours_per_week", "native_country", "income"
    ]
    df.dropna(inplace=True)
    df["income"] = df["income"].apply(lambda x: 1 if x.strip() == ">50K" else 0)

    cat_cols = ["workclass", "education", "marital_status", "occupation",
                "relationship", "race", "sex", "native_country"]
    label_encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    num_cols = ["age", "fnlwgt", "education_num", "capital_gain", "capital_loss", "hours_per_week"]
    scaler = StandardScaler()
    df[num_cols] = scaler.fit_transform(df[num_cols])

    cleaned_path = "/tmp/adult_clean_label_encoded.csv"
    encoders_path = "/tmp/label_encoders.pkl"
    scaler_path = "/tmp/scaler.pkl"

    df.to_csv(cleaned_path, index=False)
    joblib.dump(label_encoders, encoders_path)
    joblib.dump(scaler, scaler_path)

    try:
        s3.upload_file(cleaned_path, bucket_name, "preprocessed/adult_clean_label_encoded.csv")
        s3.upload_file(encoders_path, bucket_name, "preprocessed/label_encoders.pkl")
        s3.upload_file(scaler_path, bucket_name, "preprocessed/scaler.pkl")
        print("File caricati su S3.")
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Errore upload su S3: {str(e)}"
        }

    # Invoca Lambda training direttamente, senza trigger S3
    try:
        lambda_client = boto3.client("lambda")
        response = lambda_client.invoke(
            FunctionName="model_training", 
            InvocationType="Event",  # asincrona
            Payload=json.dumps({
                "source": "preprocessing",
                "s3_bucket": bucket_name,
                "s3_key": "preprocessed/adult_clean_label_encoded.csv"
            })
        )
        print(f"Invocata Lambda training, status: {response['StatusCode']}")
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Errore invocando Lambda training: {str(e)}"
        }

    return {
        'statusCode': 200,
        'body': "Preprocessing completato e Lambda training invocata."
    }
