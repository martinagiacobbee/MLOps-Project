FROM public.ecr.aws/lambda/python:3.10

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy function code
COPY inference.py .

# Set the CMD to your handler (file.function)
CMD ["inference.lambda_handler"]
