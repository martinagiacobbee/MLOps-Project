# lambda-preprocessing/Dockerfile
FROM public.ecr.aws/lambda/python:3.12

# Copia i file necessari (es. lambda_function.py, requirements.txt ecc.)
COPY preprocessing_lambda.py   ${LAMBDA_TASK_ROOT}/

# Se hai requirements, installali (opzionale)
# COPY requirements.txt  .
# RUN pip install -r requirements.txt

# Comando per avviare la lambda (funzione specifica)
CMD ["preprocessing_lambda.lambda_handler"]
