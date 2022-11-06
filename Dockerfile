FROM python:3.10-alpine

RUN pip install -U pip
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . /app
WORKDIR /app
CMD ["python3", "app.py"]
