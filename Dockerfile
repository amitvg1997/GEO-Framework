FROM public.ecr.aws/lambda/python:3.13

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./app.py
COPY metrics ./metrics

CMD [ "app.lambda_handler" ]
