
'''
vedendo le prestazioni in termini di accuracy e precision nel sito del dataset, scelgo di valorizzare la precisione 
usando RandomForest 
'''

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Carica dataset già preprocessato
df = pd.read_csv("adult_clean_label_encoded.csv")

# Separazione feature e target
X = df.drop("income", axis=1)
y = df["income"]

# Suddivisione train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Inizializzazione e addestramento modello Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Valutazione
y_pred = model.predict(X_test)

# Salva modello su disco
joblib.dump(model, "random_forest_model.pkl")
print("\n💾 Modello salvato come 'random_forest_model.pkl'")
