FROM python:3.13.12-slim-bookworm

WORKDIR /home/bot

COPY . .

RUN pip install --index-url=https://pypi.tuna.tsinghua.edu.cn/simple --default-timeout=100 -r requirements.txt

CMD ["python3", "app.py"]