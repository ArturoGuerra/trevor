from python:3-buster

WORKDIR /app
COPY requirements.txt /tmp/
RUN pip install -f /tmp/requirements.txt
COPY . .

CMD ["python", "./main.py"]
