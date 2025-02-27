FROM python:3.12.3-alpine3.20@sha256:ff11a2170938ae4e4f931435fd47f64b0f6efabd471aef37d20ad58f827ba19c

COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["python", "main.py"]