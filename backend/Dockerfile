FROM python:3.8.2-slim-buster

ENV PYTHONUNBUFFERED 1

RUN mkdir /backend

WORKDIR /backend

COPY . /backend

RUN apt-get update
RUN apt-get install -y cmake
RUN apt-get install -y wget

RUN wget https://github.com/libgit2/libgit2/archive/v0.24.0.tar.gz && \
tar xzf v0.24.0.tar.gz && \
cd libgit2-0.24.0/ && \
cmake . && \
make && \
make install

RUN ldconfig

RUN pip install -r /backend/requirements.txt

VOLUME /backend

EXPOSE 8080

CMD python /backend/API/manage.py makemigrations &&\
    python /backend/API/manage.py migrate

# docker build -t api-builder-api:latest .
# To run: docker run -d -p 8000:8000 --name API api-api-builder-api:latest