#Deriving the latest base image
FROM python:latest


#Labels as key value pair
LABEL Maintainer="smonk333"

WORKDIR /var/run/secrets

COPY auth.py ./

CMD [ "python", "./auth.py"]