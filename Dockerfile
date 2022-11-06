FROM python:3.10-alpine

RUN pip install -U pip
RUN pip install flask
EXPOSE 5000
COPY . /app
WORKDIR /app
CMD ["python3", "app.py"]
