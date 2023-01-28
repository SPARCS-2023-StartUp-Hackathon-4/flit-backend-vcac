FROM ubuntu:18.04

MAINTAINER JSK invalidid56@snu.ac.kr

RUN apt-get update
RUN apt-get update
RUN apt-get install -y --no-install-recommends python3.8 python3.8-dev python3-pip
RUN apt-get install -y git

RUN python3.8 -m pip install pip --upgrade

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./app .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--reload", ,"host=0.0.0.0", "--port=8080"]
