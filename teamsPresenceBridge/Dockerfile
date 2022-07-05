# set base image (host OS)
ARG BUILD_FROM
FROM $BUILD_FROM

# set the working directory in the container
WORKDIR /app

# set env tag
ENV RUN_IN_DOCKER Yes

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src .

# command to run on container start
CMD [ "python", "-u", "./server.py" ]
