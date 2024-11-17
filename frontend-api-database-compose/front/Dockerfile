FROM node:18 AS builder
WORKDIR /app
COPY app/package*.json ./ 
RUN npm install
COPY app/ ./ 
RUN npm run build

FROM httpd:2.4
COPY --from=builder /app/dist/ /usr/local/apache2/htdocs/
EXPOSE 80