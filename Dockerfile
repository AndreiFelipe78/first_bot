FROM python:3.9.12-bullseye

WORKDIR /app
RUN mkdir pictures

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY meu_bot.py .
COPY credencials.py .

CMD ["python", "meu_bot.py"]
