## Try to use a slimmer version of python

FROM python:3.9.14-slim
#FROM python:3.8.14
#FROM python:3.9.14-bullseye

#ENV C_FORCE_ROOT=true
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# quietly add a user without password
RUN adduser --quiet --disabled-password --shell /bin/bash --home /home/olegh --gecos "User" olegh

# set password
RUN echo "olegh:1234" | chpasswd

# Make sure to run mkhomedir_helper command as root or user with sudo access.
RUN mkhomedir_helper olegh


WORKDIR /home/olegh/app

## Trying to solve the following issue connecting to Celery
## https://stackoverflow.com/questions/53037874/docker-celery-tells-me-not-to-run-as-root-but-once-i-dont-i-lack-permission
#RUN useradd -ms /bin/bash celery


COPY requirements_my.txt /home/olegh/app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -U mljar-mercury

## Copying the code:

COPY centroid_calc_mercury.ipynb .
COPY centroid_util_colab.py .

## Trying to solve the following issue connecting to Celery
#RUN chown -R celery:celery /app
#USER celery

## Launch the application, Mercury 

EXPOSE 8000

#CMD login
CMD chmod 777 app/*.*
CMD cd app
CMD mercury run centroid_calc_mercury.ipynb
#CMD runuser -u olegh -- mercury run centroid_calc_mercury.ipynb
#CMD /bin/sh

## Mercury runs the app at port 8000 from browser:
#     http://localhost:8000

## Ref: https://medium.com/aiguys/docker-for-dummies-8e8edc8af0ea
## Build the image:
#   $ docker build -t centroid .
## Run a container:
#   $ docker run -p 8000:8000 centroid