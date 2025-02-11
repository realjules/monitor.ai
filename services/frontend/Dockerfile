# Development stage only
FROM node:18-slim

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies with caching
RUN --mount=type=cache,target=/root/.npm \
    npm install

# Set environment variables
ENV PORT=52209 \
    HOST=0.0.0.0 \
    NODE_ENV=development \
    VITE_API_URL=http://localhost:52209

# Start the development server (code will be mounted as a volume)
CMD ["npm", "run", "dev"]