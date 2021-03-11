FROM python:3.8
ENV PYTHONUNBUFFERED 1
ADD requirements.txt /root/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /root/requirements.txt --no-cache-dir

ADD . /code
WORKDIR /code

EXPOSE 8080

CMD [ "python", "main.py" ]
