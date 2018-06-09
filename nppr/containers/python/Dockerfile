FROM python:3
RUN mkdir /www
WORKDIR /www
ADD data/requirements.txt /www/
RUN export WEB_ENV=pro
RUN pip install -r requirements.txt