FROM mcr.microsoft.com/devcontainers/python:3.12

WORKDIR /workspace

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --user -r /tmp/requirements.txt \
      && python -m ipykernel install --user --name "codespace-env" --display-name "Python (codespace-env)"
