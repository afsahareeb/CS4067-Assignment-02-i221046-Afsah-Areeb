FROM node:18-alpine

WORKDIR /app

# Copy package.json and install dependencies first (Docker caching)
COPY package.json package-lock.json ./
RUN npm install

# Copy rest of the frontend code
COPY . .

EXPOSE 3000

CMD ["npm", "start"]
