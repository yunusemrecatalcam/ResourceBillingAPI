FROM python:3.7-alpine
RUN apk add binutils libc-dev
RUN pip install flask==1.1.2 gunicorn==20.0 requests==2.24.0
COPY . /app
WORKDIR /app
CMD ["gunicorn", "-w 4", "wsgi:app"]