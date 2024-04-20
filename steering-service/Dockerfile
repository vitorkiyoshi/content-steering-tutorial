FROM python:3.11-alpine


RUN adduser -D steering
USER steering
WORKDIR /home/steering

ENV PATH="/home/steering/.local/bin:${PATH}"
ENV PYTHONUNBUFFERED=1

COPY src/app.py /home/steering/
COPY src/builder.py /home/steering/
COPY src/monitoring.py /home/steering/

COPY .env /home/steering/
COPY requirements.txt /home/steering/

RUN pip install -r requirements.txt


CMD [ "python", "app.py" ]
