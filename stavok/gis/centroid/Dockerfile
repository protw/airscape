## Try to use a slimmer version of python

FROM python:3.8.14-slim

WORKDIR /app

## Two ways to create requirements.txt:
#   $ pip freeze > requirements.txt
#   $ conda list -e > requirements.txt

COPY requirements.txt .

RUN pip install -r requirements.txt

## Copying the code:

COPY centroid_calc_mercury.ipynb .
COPY centroid_util_colab.py .

## Launch the application, Mercury 

EXPOSE 8000

CMD mercury run centroid_calc_mercury.ipynb

## Mercury runs the app at port 8000 from browser:
#     http://127.0.0.1:8000

## Ref: https://medium.com/aiguys/docker-for-dummies-8e8edc8af0ea
## Build the image:
#   $ docker build .
## Run a container:
#   $ docker run --name centroid -p 8000:8000 -d <6899ea>