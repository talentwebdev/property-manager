FROM python:3.7-alpine

# running python in unbuffered, avoid complications
ENV PYTHONUNBUFFERED 1

# copy file to docker image
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# empty folder on our docker image
RUN mkdir /app
# switch to default direction in docker container
WORKDIR /app
# copy from our local mahcine to app folder in docker image
COPY ./app /app

# add user -D create a user for running applications only
RUN adduser -D user
# switches docker to user we created
# this is for security purpose, limits scope for this user 
USER user 