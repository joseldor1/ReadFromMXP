FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# ENTRYPOINT lets you pass args when running the container
ENTRYPOINT ["python", "read-mxp.py"]