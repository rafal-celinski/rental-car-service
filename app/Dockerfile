FROM node:14
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build
RUN npm install -g serve
EXPOSE 5000
ENTRYPOINT ["serve", "-s", "build", "-l", "5000"]