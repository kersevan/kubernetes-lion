# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
# COPY ./backend  /app
COPY .  /app

# Install any needed packages specified in requirements.txt
RUN ls
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 30002

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "backend.py"]