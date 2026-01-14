FROM public.ecr.aws/lambda/python:3.13

# Install system dependencies using apt-get (Debian-based image)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      gcc \
      libxml2-dev \
      libxslt1-dev \
      libssl-dev \
      build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python deps
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py ./app.py
COPY metrics ./metrics

# Lambda handler
CMD [ "app.lambda_handler" ]
