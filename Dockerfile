FROM docker:29-cli

RUN apk add --no-cache python3 py3-pip docker-cli-compose \
    || apk add --no-cache python3 py3-pip

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

COPY bot.py config.py helpers.py docker_cli.py protection.py ./
COPY commands ./commands
COPY events ./events

ENV PYTHONUNBUFFERED=1

CMD ["python", "bot.py"]
