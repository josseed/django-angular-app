FROM ubuntu:bionic

RUN apt update && apt upgrade -y
RUN apt install redis-server -y

COPY ./redis.conf /etc/redis/redis.conf

EXPOSE 6379

