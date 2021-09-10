# https://github.com/cypress-io/cypress-docker-images/blob/master/browsers/node12.16.2-chrome81-ff75/Dockerfile

FROM cypress/browsers:node12.16.2-chrome81-ff75

# japanese
RUN apt-get install -y locales locales-all
RUN apt-get remove fonts-vlgothic
RUN apt-get install -y fonts-vlgothic
RUN locale-gen ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LC_CTYPE ja_JP.UTF-8
RUN localedef -f UTF-8 -i ja_JP ja_JP.utf8

RUN apt-get install --no-install-recommends -y fonts-noto fonts-noto-cjk