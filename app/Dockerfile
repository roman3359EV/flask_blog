FROM python:3.10-alpine AS builder

RUN apk add tzdata
RUN ln -fs /usr/share/zoneinfo/Etc/GMT+3 /etc/localtime

WORKDIR /app
ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY . /app
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "flask db migrate \
    && flask db upgrade \
    && gunicorn --bind 0.0.0.0:5050 app:app"]

