FROM PROVIDE LATEST NODEJS BASE IMAGE
 
RUN node -v
 
RUN npm -v
 
USER root
 
RUN mkdir -p /app
 
WORKDIR /app
 
COPY package.json /app
 
COPY .npmrc /app

# RUN npm install -g npm@10.8.1
 
RUN npm install --legacy-peer-deps
 
COPY . /app
 
EXPOSE 30055
 
ENTRYPOINT ["npm", "start" ]
