FROM python:3-alpine
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
WORKDIR  /usr/src/app/
COPY . /usr/src/app/
EXPOSE 5000
CMD export FLASK_APP=app.py ; flask run --host 0.0.0.0