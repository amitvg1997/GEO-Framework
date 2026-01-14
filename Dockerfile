FROM public.ecr.aws/lambda/python:3.13

RUN yum install -y \
      gcc \
      libxml2-devel \
      libxslt-devel \
      openssl-devel \
      && yum clean all

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./app.py
COPY metrics ./metrics

CMD [ "app.lambda_handler" ]
