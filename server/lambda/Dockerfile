FROM public.ecr.aws/lambda/python:3.8

COPY requirements.txt ./
COPY classifier.json ./
COPY classifier.h5 ./
COPY lambda_function.py ./

RUN python3.8 -m pip install -r requirements.txt

CMD ["lambda_function.lambda_handler"]
