# Base runtime image
FROM node:20-slim

# Set working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy in the code
COPY . .

# Expose port
EXPOSE 3000

# Run the app
CMD ["npm", "run", "dev", "--","-H", "0.0.0.0"]