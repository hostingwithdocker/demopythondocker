FROM python:3.6.8-alpine3.9

ENV PIPENV_VENV_IN_PROJECT=1
WORKDIR /app
COPY ./ /app
RUN apk update && apk add bash tzdata &&\
    cp /usr/share/zoneinfo/Asia/Singapore /etc/localtime &&\
    pip install --upgrade setuptools pip wheel pipenv &&\
    pipenv install

EXPOSE 8080
CMD ["/bin/bash","/app/run-container.sh"]