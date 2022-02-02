FROM python:3.7-buster
ARG PIP_USERNAME
ARG PIP_PASSWORD
WORKDIR /usr/src/app
COPY requirements.txt .
COPY internal_requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && chmod +x gunicorn_starter.sh
RUN PIP_USERNAME=$PIP_USERNAME PIP_PASSWORD=$PIP_PASSWORD pip install --no-cache-dir -r internal_requirements.txt
COPY . .
CMD ["./gunicorn_starter.sh"]
