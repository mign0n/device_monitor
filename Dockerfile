FROM python:3.13-slim
WORKDIR /device_monitor

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
