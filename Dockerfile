FROM bitnami/spark:latest

USER root 

RUN adduser --disabled-password --gecos '' --uid 1001 sparkuser

USER sparkuser 

WORKDIR /opt/workspace
#