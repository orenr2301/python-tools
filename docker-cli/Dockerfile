FROM alpine:latest

RUN apk add --no-cache python3 py3-pip

WORKDIR /app

RUN apk add --no-cache curl net-tools

EXPOSE 8000

CMD ["python3", "-m", "http.server", "8000"]

