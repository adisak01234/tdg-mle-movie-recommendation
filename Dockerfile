# Use the tiangolo/uwsgi-nginx-flask image as the base image
FROM tiangolo/uwsgi-nginx-flask:python3.11

# Set the working directory in the container
WORKDIR /

COPY requirements.txt /

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Now copy the rest of the application code, this layer is rebuilt when code changes
COPY . /

# Expose the port on which the app will run
EXPOSE 80

# uWSGI configuration (optional, if you have specific settings)
# For example, to set the number of uWSGI workers:
# ENV UWSGI_CHEAPER 2
# ENV UWSGI_PROCESSES 4

# By default, this image expects the entry point to be at /app/main.py
# If your app entry point is different, you need to set the `APP_MODULE` environment variable
ENV APP_MODULE=app.main:app

