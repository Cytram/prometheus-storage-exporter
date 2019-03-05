FROM python:3.7.0-alpine
LABEL maintainer "Jesper Petersen"
LABEL mail "jp@onlinecity.dk"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./
CMD ["/usr/local/bin/gunicorn", "-b", "0.0.0.0:9405", "-t", "180", "main:app"]
