import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Carica il dataset
df = pd.read_csv("adult.data", header=None, na_values="?", skipinitialspace=True)

# Nomi delle colonne
df.columns = [
    "age", "workclass", "fnlwgt", "education", "education_num",
    "marital_status", "occupation", "relationship", "race", "sex",
    "capital_gain", "capital_loss", "hours_per_week", "native_country", "income"
]

# Rimuove righe con valori mancanti
df.dropna(inplace=True)

# Codifica la colonna target
df["income"] = df["income"].apply(lambda x: 1 if x.strip() == ">50K" else 0)

# Elenco colonne categoriali da label-encodare
cat_cols = ["workclass", "education", "marital_status", "occupation",
            "relationship", "race", "sex", "native_country"]

# Applica Label Encoding
label_encoders = {}
for col in cat_cols:
    le = LabelEncoder() #assegna valori numerici a valori categorici
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le  # Salva encoder se vuoi usarlo su dati futuri

# Normalizzazione delle colonne numeriche
num_cols = ["age", "fnlwgt", "education_num", "capital_gain", "capital_loss", "hours_per_week"]
scaler = StandardScaler()
df[num_cols] = scaler.fit_transform(df[num_cols])

# Salva dataset trasformato
df.to_csv("adult_clean_label_encoded.csv", index=False)

print("✅ Preprocessing completato. Dataset salvato come 'adult_clean_label_encoded.csv'") #in aws carico il df modificato nel nuovo bucket
