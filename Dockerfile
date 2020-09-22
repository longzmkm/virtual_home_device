FROM python:3.7-alpine


RUN apk --update add --no-cache g++
ADD ./requirements.txt /code/requirements.txt
WORKDIR /code

RUN pip install --no-cache-dir -r  requirements.txt

ADD . .
CMD ["python","./hapi/manage.py"]