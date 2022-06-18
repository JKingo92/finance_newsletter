FROM python:3.10.0

LABEL MAINTAINER = "Jonathan Kingo"
WORKDIR /newsletter
COPY . /newsletter
RUN pip3 install -r requirements.txt
CMD [ "python", "./newsletter.py" ]