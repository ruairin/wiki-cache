FROM python:3.11.4-alpine3.17

# Installing client libraries and any other package you need
RUN apk update && apk add libpq

# Installing build dependencies
# These are required for psycopg2
RUN apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["waitress-serve", "--listen=*:5000", "app:app"]
