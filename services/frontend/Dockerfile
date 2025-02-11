FROM node:18-slim

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Set environment variables
ENV PORT=52209
ENV HOST=0.0.0.0
ENV NODE_ENV=production

# Build the application
RUN npm run build

# Start the application
CMD ["npm", "run", "dev"]