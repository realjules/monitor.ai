# Build stage
FROM node:18-slim as builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies with caching
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Copy application code
COPY . .

# Build the application
RUN npm run build

# Development stage
FROM node:18-slim

WORKDIR /app

# Copy package files and install dependencies with caching
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Copy source code for development
COPY . .

# Set environment variables
ENV PORT=52209 \
    HOST=0.0.0.0 \
    NODE_ENV=development

# Start the development server
CMD ["npm", "run", "dev"]