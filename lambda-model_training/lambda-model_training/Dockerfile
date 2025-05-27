# lambda-model_training/Dockerfile
FROM public.ecr.aws/lambda/python:3.12

COPY model_training_lambda.py  ${LAMBDA_TASK_ROOT}/

# Install requirements se serve
# COPY requirements.txt  .
# RUN pip install -r requirements.txt

CMD ["model_training_lambda.lambda_handler"]
