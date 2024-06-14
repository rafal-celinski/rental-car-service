# Use an official Node runtime as a parent image
FROM node:14

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install dependencies
RUN npm install

# Build the app for production with minification
RUN npm run build

# Install serve globally
RUN npm install -g serve

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV REACT_APP_API_URL=http://api:8080

# Run serve when the container launches
ENTRYPOINT ["serve", "-s", "build", "-l", "5000"]
