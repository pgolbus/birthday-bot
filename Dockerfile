FROM python:3

WORKDIR /usr/src/app

COPY requirements.lock ./
RUN pip install --no-cache-dir -r requirements.lock

COPY . .

CMD [ "python", "./bot.py" ]