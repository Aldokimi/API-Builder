FROM node:slim AS build

WORKDIR /app

COPY package.json ./

COPY package-lock.json ./

RUN npm install

COPY . ./

EXPOSE 5173
