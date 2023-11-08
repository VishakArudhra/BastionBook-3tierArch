FROM --platform=linux/x86_64 python:3.11-slim

# updating repositories
RUN apt-get update

# installing essential packages
RUN apt-get install -y xz-utils
RUN apt install -y unzip
RUN apt install -y curl
RUN apt install -y less
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install

# permissions and bas10book user for tightened security
RUN useradd -m -u 1500 --shell /bin/bash bas10book
RUN mkdir -p /home/bas10book/backend && \
    mkdir -p /home/bas10book/.aws && \
    chown -R bas10book:bas10book /home/bas10book 
USER bas10book
WORKDIR /home/bas10book/backend

# copying application files into the image
COPY --chown=bas10book:bas10book . .

# creating python environment
ENV VIRTUAL_ENV=/home/bas10book/backend/.venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN export FLASK_APP=lambda-backend-flask.py
RUN pip install -r requirements.txt
SHELL ["/bin/bash", "-c"]

# for difference between entrypoint and cmd: 
# https://stackoverflow.com/questions/21553353/what-is-the-difference-between-cmd-and-entrypoint-in-a-dockerfile

# docker run -p 5001:5000 -platform linux/x86_64 -v ./.aws:/home/bas10book/.aws bas10book-backend 
ENTRYPOINT ["python3", "bastionbookBackend.py"]
