# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

RUN pip install --upgrade pip
# define the present working directory
RUN pip install virtualenv
ENV VIRTUAL_ENV=/venv
RUN virtualenv venv -p python3
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Set environment variable
ENV FLASK_APP app.py

# Expose the port on which the app will run
EXPOSE 5000

# Run the command to start the Flask server
CMD ["python","app.py"]
