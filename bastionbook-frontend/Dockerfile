FROM python:3.11-slim

# upgrade pip
RUN pip install --upgrade pip

# updating respositories
RUN apt-get update
RUN apt-get install xz-utils

# get curl for healthchecks
RUN apt install -y curl

# permissions and nonroot user for tightened security
RUN adduser nonroot
RUN mkdir /home/app/ && chown -R nonroot:nonroot /home/app
WORKDIR /home/app
USER nonroot

# copy all the files to the container
COPY --chown=nonroot:nonroot . .

#venv
ENV VIRTUAL_ENV=/home/app/venv

# python setup
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN export FLASK_APP=bastionbook.py
RUN pip install -r requirements.txt

# define the port number the container should expose

CMD ["python3", "bastionbook.py"]