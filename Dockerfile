FROM python:3.11-alpine

WORKDIR /app
COPY . .
RUN apk update && apk upgrade && apk add --no-cache git
RUN python -m pip install -r requirements.txt && python -m pip install git+https://gitlab.com/mailman/mailmanclient

CMD ["python3", "main.py"]
