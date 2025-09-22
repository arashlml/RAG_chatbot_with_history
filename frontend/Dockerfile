FROM python:3.12-slim

WORKDIR /app/frontend

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR /app

CMD ["streamlit","run","frontend/app.py"]