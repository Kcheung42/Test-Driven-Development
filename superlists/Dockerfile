FROM python:3.6.2
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app
ADD requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
COPY . /usr/src/app

CMD ["/usr/src/app/entrypoint.sh"]

