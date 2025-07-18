FROM python:3.11-slim-buster

WORKDIR /python-docker
RUN mkdir -p /tmp && chmod 1777 /tmp

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src .

EXPOSE 8080
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "main:app"]
