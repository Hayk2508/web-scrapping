#use official python image
FROM python:3.10-slim

# Set the working directory 
WORKDIR /app

# Copy the requirements file into  container
COPY requirements.txt requirements.txt



# Install the all the required dependencies 

RUN pip install -r requirements.txt


# Copy the rest of the application code into container
COPY . .


EXPOSE 8000


# command to run the application
CMD ["python", "web-server/manage.py", "runserver", "0.0.0.0:8000"] 
