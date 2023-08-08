FROM python:3.8-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./articles /app/articles

COPY ./server.py /app/server.py

COPY ./model /app/model

COPY ./build /app/build

CMD ["sh", "-c", "uvicorn server:app --host 0.0.0.0 --port $PORT"]
