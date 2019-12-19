
FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y ca-certificates
RUN update-ca-certificates

COPY sources.list /etc/apt

RUN apt-get -y update
RUN apt-get install -f -y chromium-browser python3-pip xvfb

RUN mkdir -p /src

COPY requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt
