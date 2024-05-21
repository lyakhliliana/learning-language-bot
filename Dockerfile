FROM python:latest
RUN pip install pyTelegramBotAPI==4.8.0
RUN pip install googletrans==4.0.0-rc1
RUN pip install python-telegram-bot==12.2.0
RUN mkdir  -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app
CMD ["python", "main.py"]