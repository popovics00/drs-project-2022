FROM alpine:latest

RUN apk add --no-cache python3-dev \
    && apk add py3-pip \
    && pip3 install --upgrade pip

WORKDIR /app

COPY . /app

RUN pip --no-cache-dir install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["main.py"]