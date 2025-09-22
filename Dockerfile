FROM python:3.12-slim

WORKDIR /app/chatbot

COPY chatbot/requirements.txt .

RUN pip install -r requirements.txt

COPY ./chatbot .

COPY .env .

WORKDIR /app

CMD ["uvicorn", "chatbot.main:app", "--host", "0.0.0.0", "--port", "8001"]
