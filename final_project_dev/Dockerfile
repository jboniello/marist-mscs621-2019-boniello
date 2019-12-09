FROM python:3.6

LABEL maintainer="jason.boniello1@marist.edu"

EXPOSE 5000

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
