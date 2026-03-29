FROM python:3.13.12-slim-bookworm

WORKDIR /home/bot

COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "app.py"]