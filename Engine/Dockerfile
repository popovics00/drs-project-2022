FROM alpine:latest

RUN apk add python3-dev \
    && apk add py3-pip \
    && apk add gcc \
    && apk add g++ \
    && pip3 install --upgrade pip \
    && apk update \
    && apk add musl-dev mariadb-dev gcc \
    && pip3 install mysqlclient 
    
WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["main.py"]