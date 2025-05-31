
# 🚀 MLOps-Project on AWS

## 🌐 Overview

This project implements a full **MLOps pipeline** using **AWS cloud services** to automate every step — from data ingestion to model deployment. It’s designed for **scalability**, **automation**, and **reproducibility**, making it suitable for production-ready machine learning workflows.

---

## 🧠 Purpose

The goal is to demonstrate a real-world, event-driven MLOps architecture where:

* 📦 Data ingestion, preprocessing, training, and inference are each handled by modular Lambda functions
* ☁️ The system is orchestrated entirely using AWS services for ease of deployment and scaling

---

## ☁️ AWS Architecture

### 🔧 Architecture Diagram

```plaintext
               +-------------+
               |             |
               |   Client    |
               | (Uploader)  |
               |             |
               +------|------+
                      |
                      | 1. Upload raw data
                      v
             +-------------------+
             |    S3 Bucket      |
             |    /raw/          |
             +--------|----------+
                      |
                      | 2. Trigger
                      v
         +---------------------------+
         | Lambda: Data Preprocessing|
         +-------------|-------------+
                       |
         3. Save preprocessed data
                       v
             +-------------------+
             |    S3 Bucket      |
             |  /preprocessed/   |
             +--------|----------+
                      |
                      | 4. Trigger
                      v
           +------------------------+
           | Lambda: Model Training |
           +------------|-----------+
                        |
           5. Save trained model
                        v
              +------------------+
              |   S3 Bucket      |
              |    /model/       |
              +-------|----------+
                      |
                      | 6. On API Call
                      v
            +---------------------+
            | Lambda: Inference   |
            +--------|------------+
                     |
           7. Return prediction
                     v
              +-------------+
              |  Client/API |
              +-------------+
```

---

## 🧭 Execution Flow

1. **📥 Upload Dataset to S3 (/raw)**
   A CSV file is uploaded to `s3://<bucket>/raw/`.

2. **⚙️ Lambda 1: Preprocessing**

   * Triggered automatically.
   * Cleans and formats the raw data.
   * Saves cleaned data to `s3://<bucket>/preprocessed/`.

3. **🧠 Lambda 2: Model Training**

   * Triggered by the preprocessed data.
   * Trains a model and saves it to `s3://<bucket>/model/`.

4. **🌐 Lambda 3: Inference**

   * Invoked via API Gateway (HTTP POST request).
   * Loads the model and returns predictions.

---

## 📁 Project Structure

```
MLOps-Project/
├── lambda-model_training/    # Model training logic
├── lambda-preprocessing/     # Data preprocessing logic
├── lambda_inference/         # Inference logic for predictions
├── app.py                    # Flask API (for local testing)
├── requirements.txt          # Project dependencies
└── README.md
```

---

## 🛠️ AWS Services Used

| AWS Service     | Description                                      |
| --------------- | ------------------------------------------------ |
| **S3**          | Stores datasets (raw, preprocessed) and models   |
| **Lambda**      | Serverless compute for each step in the pipeline |
| **ECR**         | Hosts Docker images with all dependencies        |
| **API Gateway** | Web entry point to trigger inference             |

---

## 🚀 Getting Started

### ✅ Prerequisites

* Python 3.8+
* Docker
* AWS CLI configured
* AWS account with access to Lambda, S3, ECR, API Gateway

---

## ⚙️ Setup & Deployment

1. **Clone the Repo**

   ```bash
   git clone https://github.com/martinagiacobbee/MLOps-Project.git
   cd MLOps-Project
   ```

2. **Build and Push Docker Images to ECR**

   Example for preprocessing Lambda:

   ```bash
   cd lambda-preprocessing
   docker build -t preprocessing .
   aws ecr create-repository --repository-name preprocessing
   docker tag preprocessing:latest <aws_id>.dkr.ecr.<region>.amazonaws.com/preprocessing
   docker push <aws_id>.dkr.ecr.<region>.amazonaws.com/preprocessing
   ```

   Repeat for `model_training` and `inference`.

3. **Deploy Lambdas via Console or IaC (e.g., Terraform)**

   * Link ECR images
   * Configure S3 triggers and API Gateway endpoints

---

## 📡 Inference API Example

After deployment:

```bash
curl -X POST https://<api-id>.execute-api.<region>.amazonaws.com/prod/predict \
     -H "Content-Type: application/json" \
     -d '{"feature1": value1, "feature2": value2, ...}'
```

---

## 🌟 Features

* ✅ Serverless, containerized ML pipeline
* 🔄 Event-driven with full automation
* ☁️ Fully deployed using AWS cloud infrastructure
* 🧩 Modular design for easy customization

---

## 📬 Contact

Created by [Martina Giacobbe](https://github.com/martinagiacobbee)
For questions or feedback, feel free to reach out via GitHub.


