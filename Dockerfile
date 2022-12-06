# use python 3 base image
FROM python:3
# set working directory for container
WORKDIR /app
# copy  all files into container app directory
ADD . /app
# install dependency  inside container
RUN pip install -r requirements.txt
#run server
CMD python manage.py runserver 0.0.0.0:8080