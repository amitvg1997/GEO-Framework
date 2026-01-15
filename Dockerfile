FROM public.ecr.aws/lambda/python:3.13

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data for textstat
RUN python -c "import nltk; nltk.download('cmudict', quiet=True)"

# Download spacy model
RUN python -m spacy download en_core_web_sm

# Copy application code
COPY app.py ./app.py
COPY metrics ./metrics

CMD [ "app.lambda_handler" ]
