# Use the latest Node.js image
FROM node:latest

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json from the src folder
COPY src/package*.json ./ 

# Install dependencies
RUN npm install

# Copy the entire application into the container
COPY . .

# Set the working directory for the application
WORKDIR /usr/src/app/src

# Expose the port for the development server
EXPOSE 5173

# Start the development server
CMD ["npm", "run", "dev", "--", "--host"]