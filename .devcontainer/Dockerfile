FROM mcr.microsoft.com/devcontainers/python:3.12

WORKDIR /workspace

COPY requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONPATH=/workspace:$PYTHONPATH
