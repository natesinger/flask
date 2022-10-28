FROM python:3.11-rc-bullseye 

COPY app /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["./run_server.sh"]
