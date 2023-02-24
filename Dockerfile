FROM python:3.9 

COPY . /bw_api

WORKDIR /bw_api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -r /bw_api/requirements.txt && rm -rf /root/.cache/pip

CMD uvicorn main:app --host 0.0.0.0 --port 8000

