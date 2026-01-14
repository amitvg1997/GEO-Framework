FROM public.ecr.aws/lambda/python:3.13

# Just install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py ./app.py
COPY metrics ./metrics

# Lambda handler
CMD [ "app.lambda_handler" ]

