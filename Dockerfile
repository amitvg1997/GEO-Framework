FROM public.ecr.aws/lambda/python:3.13

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Create nltk_data directory and download cmudict into it
RUN mkdir -p /var/task/nltk_data && \
    python -c "import nltk; nltk.data.path.insert(0, '/var/task/nltk_data'); nltk.download('cmudict', download_dir='/var/task/nltk_data', quiet=True)"

# Download spacy model
RUN python -m spacy download en_core_web_sm

# Copy application code
COPY app.py ./app.py
COPY metrics ./metrics

CMD [ "app.lambda_handler" ]
