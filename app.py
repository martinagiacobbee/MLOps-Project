import streamlit as st
import boto3
import json
import os
from dotenv import load_dotenv

# Carica le variabili dal file local.env (se il file si chiama local.env e sta nella stessa cartella)
load_dotenv('local.env')

# Ora puoi leggere le variabili d'ambiente
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')

# Imposta il client boto3 Lambda (opzionalmente con credenziali esplicite)
lambda_client = boto3.client('lambda',
    region_name='eu-west-3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

st.set_page_config(page_title="Predizione Reddito >50K", page_icon="💰", layout="centered")
st.title("💰 Predizione Reddito")

with st.form("prediction_form"):
    st.subheader("Inserisci i dati")

    age = st.number_input("Età", min_value=0)
    workclass = st.selectbox("Workclass", [
        "Private", "Self-emp-not-inc", "Self-emp-inc", "Federal-gov", "Local-gov", "State-gov",
        "Without-pay", "Never-worked"
    ])
    fnlwgt = st.number_input("Fnlwgt", min_value=0) #final sampling weight
    education = st.selectbox("Educazione", [
        "Bachelors", "Some-college", "11th", "HS-grad", "Prof-school", "Assoc-acdm",
        "Assoc-voc", "9th", "7th-8th", "12th", "Masters", "1st-4th", "10th",
        "Doctorate", "5th-6th", "Preschool"
    ])
    education_num = st.number_input("Numero anni educazione", min_value=0)
    marital_status = st.selectbox("Stato civile", [
        "Married-civ-spouse", "Divorced", "Never-married", "Separated", "Widowed",
        "Married-spouse-absent", "Married-AF-spouse"
    ])
    occupation = st.selectbox("Occupazione", [
        "Tech-support", "Craft-repair", "Other-service", "Sales", "Exec-managerial",
        "Prof-specialty", "Handlers-cleaners", "Machine-op-inspct", "Adm-clerical",
        "Farming-fishing", "Transport-moving", "Priv-house-serv", "Protective-serv",
        "Armed-Forces"
    ])
    relationship = st.selectbox("Relazione", [
        "Wife", "Own-child", "Husband", "Not-in-family", "Other-relative", "Unmarried"
    ])
    race = st.selectbox("Razza", [
        "White", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other", "Black"
    ])
    sex = st.selectbox("Sesso", ["Female", "Male"])
    capital_gain = st.number_input("Capital Gain", min_value=0)
    capital_loss = st.number_input("Capital Loss", min_value=0)
    hours_per_week = st.number_input("Ore lavorate per settimana", min_value=0)
    native_country = st.selectbox("Paese di origine", [
        "United-States", "Cambodia", "England", "Puerto-Rico", "Canada", "Germany",
        "Outlying-US(Guam-USVI-etc)", "India", "Japan", "Greece", "South", "China",
        "Cuba", "Iran", "Honduras", "Philippines", "Italy", "Poland", "Jamaica",
        "Vietnam", "Mexico", "Portugal", "Ireland", "France", "Dominican-Republic",
        "Laos", "Ecuador", "Taiwan", "Haiti", "Columbia", "Hungary", "Guatemala",
        "Nicaragua", "Scotland", "Thailand", "Yugoslavia", "El-Salvador",
        "Trinadad&Tobago", "Peru", "Hong", "Holand-Netherlands"
    ])

    submitted = st.form_submit_button("Predici")

    if submitted:
        input_data = {
            "age": age,
            "workclass": workclass,
            "fnlwgt": fnlwgt,
            "education": education,
            "education_num": education_num,
            "marital_status": marital_status,
            "occupation": occupation,
            "relationship": relationship,
            "race": race,
            "sex": sex,
            "capital_gain": capital_gain,
            "capital_loss": capital_loss,
            "hours_per_week": hours_per_week,
            "native_country": native_country
        }

        with st.spinner("Invio richiesta alla Lambda..."):
            try:
                response = lambda_client.invoke(
                            FunctionName='model_inference',
                            InvocationType='RequestResponse',
                            Payload=json.dumps({"body": json.dumps(input_data)}),  
                )       

                response_payload = json.loads(response["Payload"].read())
                body = json.loads(response_payload.get("body", "{}"))

                if "prediction" in body:
                    pred = ">50K" if body["prediction"] == 1 else "<=50K"
                    prob = f"{body['probability_of_>50K'] * 100:.2f}%"
                    st.success(f"💡 **Predizione**: {pred} \n\n📊 **Probabilità**: {prob}")
                else:
                    st.error(f"Errore nella risposta: {body.get('error', 'Sconosciuto')}")

            except Exception as e:
                st.error(f"Errore durante la chiamata Lambda: {str(e)}")
