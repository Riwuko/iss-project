FROM node:14
RUN mkdir /frontend
WORKDIR /frontend

ENV PATH /code/node_modules/.bin:$PATH
COPY /frontend/package.json ./
COPY /frontend/package-lock.json ./
RUN npm install --silent
RUN npm install react-scripts -g --silent

ADD /frontend/ /frontend/

CMD ["npm", "start"]
