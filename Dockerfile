FROM python:3.7-buster
USER root
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update
RUN apt-get install -y postfix
COPY . .
CMD ["./gunicorn_starter.sh"]
# CMD ["python","app.py"]
