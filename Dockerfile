# Pull base image
FROM python:3.7

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# dependencies를 위한 apt-get update
RUN apt-get update && apt-get -y install libpq-dev -y

RUN apt-get install libssl-dev -y

RUN apt-get install -y netcat


# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# static file
RUN python manage.py collectstatic --noinput