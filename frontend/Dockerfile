# Base image
FROM node:16

# Set working directory
WORKDIR /app

# Install dependencies
COPY src/package*.json ./
RUN npm install

# Copy project files #disable this while development
COPY src/. .



# Expose port (matches FRONTEND_PORT)
EXPOSE 5173

# Use ARG to accept build-time variables
ARG GOOGLE_CLIENT_ID
ARG SITE_URL
ARG VITE_FEEDBACK_FOLDER
ARG VITE_CV_FOLDER
ARG VITE_IMAGES_FOLDER
ARG VITE_OPENAI_AI_MODEL


# Set environment variables from build-time ARGs
ENV VITE_GOOGLE_CLIENT_ID=${VITE_GOOGLE_CLIENT_ID}
ENV VITE_SITE_URL=${SITE_URL}
ENV VITE_FEEDBACK_FOLDER=${VITE_FEEDBACK_FOLDER}
ENV VITE_CV_FOLDER=${VITE_CV_FOLDER}
ENV VITE_IMAGES_FOLDER=${VITE_IMAGES_FOLDER}
ENV VITE_OPENAI_AI_MODEL=${VITE_OPENAI_AI_MODEL}

# Start the app (adjust if your build creates a different file)
CMD ["npm", "run", "build"]