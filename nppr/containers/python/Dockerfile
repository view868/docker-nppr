FROM python:3.6
########## REQUIRED DEPENDENCIES ################
#RUN mkdir ~/.pip && \
#    cd ~/.pip/  && \
#    echo "[global] \ntimeout = 6000 \ntrusted-host =  pypi.douban.com \nindex-url = http://pypi.douban.com/simple" >  pip.conf

RUN mkdir /www
WORKDIR /www
ADD data/requirements.txt /www/
RUN export WEB_ENV=pro
RUN pip install -r requirements.txt