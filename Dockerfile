# docker container settings
# Secret folder and files needs to add MANUALLY
# Marakulin Andrey @annndruha
# 2020

# Base image
FROM python:3-alpine

# Add the main dirictory
ADD ./ gmail/

# Set that dirictory
WORKDIR gmail

# Update Base image
RUN apk update && \
    apk add --no-cache --virtual build-deps gcc python-dev musl-dev && \
    apk add --no-cache postgresql-dev && \
	pip install --no-cache-dir -r requirements.txt && \
	apk del build-deps

# Specify the port number the container should expose 
EXPOSE 1488

# Run the file
CMD ["python", "-u", "./main.py"]

# Example docker command:
# docker run -d --name gmail -v /root/gmail/secret:/gmail/secret imagename

# See logs:
# docker logs gmail --follow