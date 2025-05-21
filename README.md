
````markdown
# 🔍 Income Classification with AWS Lambda & S3

Un progetto end-to-end per la predizione del reddito (superiore o inferiore a 50K) basato sul dataset *Adult Census Income*, interamente orchestrato con **AWS Lambda**, **S3**, e **API Gateway**. L’obiettivo è creare un'infrastruttura serverless per il preprocessing, l’addestramento del modello e l’inferenza via HTTP.

---

## 📁 Architettura del Progetto

```
          ┌─────────────┐
          │ S3 Bucket   │ (raw + preprocessed + model)
          └─────┬───────┘
                │
   ┌────────────▼─────────────┐
   │ Lambda: Preprocessing    │
   │ - Pulizia                │
   │ - Encoding + Scaling     │
   └────────────┬─────────────┘
                │ triggers
   ┌────────────▼─────────────┐
   │ Lambda: Model Training   │
   │ - Random Forest          │
   │ - Salvataggio in S3      │
   └────────────┬─────────────┘
                │
   ┌────────────▼─────────────┐
   │ Lambda: Inference        │
   │ - Trigger via API GW     │
   │ - Predizione live        │
   └──────────────────────────┘
````

---

## 🚀 Componenti principali

| Funzione Lambda  | Descrizione                                                  |
| ---------------- | ------------------------------------------------------------ |
| `preprocessing`  | Carica, pulisce e normalizza il dataset. Salva output in S3. |
| `model_training` | Allena un modello Random Forest e lo salva in S3.            |
| `inference`      | Riceve input da HTTP API e restituisce la predizione.        |

---

## 🧠 Modello

* **Algoritmo**: `RandomForestClassifier` (Scikit-learn)
* **Feature Engineering**:

  * Encoding LabelEncoder per variabili categoriche
  * StandardScaler per feature numeriche

---

## 💻 Tecnologie utilizzate

* **AWS Lambda**
* **Amazon S3**
* **AWS API Gateway**
* **Python 3.12**
* **Scikit-learn, pandas, joblib**
* **GitHub + VS Code**

---

## ⚙️ Come usare il progetto

### ✅ Preprocessing

1. Carica il dataset `adult.data` su Lambda `preprocessing`
2. Output:

   * `preprocessed/adult_clean_label_encoded.csv`
   * `preprocessed/label_encoders.pkl`
   * `preprocessed/scaler.pkl`

### ✅ Addestramento

* Triggerata automaticamente al termine del preprocessing.
* Salva il modello in:

  * `model/random_forest_model.pkl`

### ✅ Inferenza via HTTP

1. Deploy della Lambda `inference` con API Gateway
2. Invia una richiesta `POST` con dati simili a:

```json
{
  "age": 45,
  "workclass": "Private",
  "fnlwgt": 284582,
  "education": "Bachelors",
  "education_num": 13,
  "marital_status": "Married-civ-spouse",
  "occupation": "Exec-managerial",
  "relationship": "Wife",
  "race": "White",
  "sex": "Female",
  "capital_gain": 0,
  "capital_loss": 0,
  "hours_per_week": 50,
  "native_country": "United-States"
}
```

3. Output:

```json
{
  "prediction": 1,
  "probability_of_>50K": 0.87
}
```

---

## 🧪 Testing

* Tutte le funzioni Lambda sono testabili da AWS Console.
* L’inferenza può essere testata anche da Postman o frontend HTTP.

---

## 📌 To Do

* [ ] Logging CloudWatch avanzato
* [ ] Gestione errori input più robusta
* [ ] Validazione dello schema JSON

---


