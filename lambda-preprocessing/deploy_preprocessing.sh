#!/bin/bash

# CONFIGURAZIONE
FUNCTION_NAME="preprocessing"
AWS_REGION="eu-west-3"
REPOSITORY_NAME="lambda-preprocessing"
IMAGE_TAG="latest"

# Ottieni Account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
IMAGE_URI="$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPOSITORY_NAME:$IMAGE_TAG"
ROLE_ARN="arn:aws:iam::$ACCOUNT_ID:role/uploadDB"

# CREA REPO ECR SE NON ESISTE
echo "🛠  Controllo o creazione del repository ECR..."
aws ecr describe-repositories --repository-names $REPOSITORY_NAME --region $AWS_REGION > /dev/null 2>&1

if [ $? -ne 0 ]; then
    aws ecr create-repository --repository-name $REPOSITORY_NAME --region $AWS_REGION
    echo "✅ Repository $REPOSITORY_NAME creato."
else
    echo "✅ Repository $REPOSITORY_NAME già esistente."
fi

# LOGIN A ECR
echo "🔐 Login a ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin "$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

# BUILD E PUSH IMMAGINE DOCKER
echo "🐳 Costruzione immagine Docker dal Dockerfile..."
docker build -t $REPOSITORY_NAME ./lambda-preprocessing

echo "🏷️  Tag immagine con URI: $IMAGE_URI"
docker tag $REPOSITORY_NAME:latest $IMAGE_URI

echo "📤 Push immagine su ECR..."
docker push $IMAGE_URI

# CREA O AGGIORNA LA FUNZIONE LAMBDA
echo "📦 Deploy della Lambda $FUNCTION_NAME..."

aws lambda get-function --function-name $FUNCTION_NAME --region $AWS_REGION > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "🆕 Creazione funzione Lambda..."
    aws lambda create-function \
        --function-name $FUNCTION_NAME \
        --package-type Image \
        --code ImageUri=$IMAGE_URI \
        --role $ROLE_ARN \
        --region $AWS_REGION \
        --timeout 900 \
        --memory-size 1024
else
    echo "♻️  Aggiornamento codice funzione Lambda..."
    aws lambda update-function-code \
        --function-name $FUNCTION_NAME \
        --image-uri $IMAGE_URI \
        --region $AWS_REGION
fi

echo "✅ Deploy completato. Funzione Lambda: $FUNCTION_NAME"
