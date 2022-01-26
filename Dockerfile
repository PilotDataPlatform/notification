FROM python:3.7-buster
ARG pip_username
ARG pip_password
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN PIP_USERNAME=$pip_username PIP_PASSWORD=$pip_password pip install --no-cache-dir -r requirements.txt && chmod +x gunicorn_starter.sh
COPY . .
CMD ["./gunicorn_starter.sh"]
