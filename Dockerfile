FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV ACCEPT_EULA=Y
RUN apt-get update && apt-get install -y curl gnupg2
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
# install dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get remove -y python3.10 && \
    apt-get install -y --no-install-recommends software-properties-common gnupg2 && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libsasl2-dev \
    libssl-dev libffi-dev \
    python3.9 python3.9-dev python3.9-venv libpython3.9-dev libpython3.9 \
    python3.9-distutils \
    odbcinst \
    msodbcsql18 \
    unixodbc-dev git && \
    apt-get clean -qq -y && \
    apt-get autoclean -qq -y && \
    apt-get autoremove -qq -y && \
    rm -rf /var/lib/apt/lists/*
RUN ln -s /usr/bin/python3.9 /usr/bin/python && \
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3.9 get-pip.py

# extra dependencies for soda-scientific
RUN pip --no-cache-dir install "numpy>=1.15.4" \
                               "Cython>=0.22"
RUN mkdir /app

WORKDIR /app

RUN pip install --upgrade pip

COPY . .

RUN pip --no-cache-dir install "$(cat dev-requirements.in | grep pip-tools)" && \
    pip --no-cache-dir install -r dev-requirements.txt

RUN pip --no-cache-dir install -r requirements.txt

RUN apt-get purge -y build-essential git curl && \
    apt-get clean -qq -y && \
    apt-get autoclean -qq -y && \
    apt-get autoremove -qq -y

ENTRYPOINT [ "soda" ]
CMD [ "scan" ]
