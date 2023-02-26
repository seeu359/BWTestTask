FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY /requirements.txt /bw_api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /bw_api/requirements.txt

COPY . /bw_api

WORKDIR /bw_api

CMD uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8000
