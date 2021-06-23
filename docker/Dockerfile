FROM nvidia/cudagl:11.0-devel-ubuntu20.04
ARG DEBIAN_FRONTEND=noninteractive

ARG PYTHON_VERSION=3.8

ARG branch

# Install ubuntu libaries
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential cmake pkg-config \
        libfreetype6-dev git nano wget curl vim ca-certificates unzip libjpeg-dev \
        libpng-dev libosmesa6-dev software-properties-common xvfb gpg-agent

# Install miniconda
RUN curl -o ~/miniconda.sh -O  https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh  && \
     chmod +x ~/miniconda.sh && \
     ~/miniconda.sh -b -p /opt/conda && \
     rm ~/miniconda.sh && \
     /opt/conda/bin/conda update -n base -c defaults conda && \
     /opt/conda/bin/conda install -y python=$PYTHON_VERSION setuptools patchelf && \
     /opt/conda/bin/conda clean -ya
ENV PATH /opt/conda/bin:$PATH


# Env vars for the nvidia-container-runtime.
ENV PATH /usr/local/cuda/bin/:$PATH
ENV LD_LIBRARY_PATH /usr/local/cuda/lib:/usr/local/cuda/lib64
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
LABEL com.nvidia.volumes.needed="nvidia_driver"

# Install weebots
RUN wget -qO- https://cyberbotics.com/Cyberbotics.asc | apt-key add -
RUN apt-add-repository 'deb https://cyberbotics.com/debian/ binary-amd64/' && \
    apt-get update &&  apt-get install -y webots

# Save enviroment libraries
ENV WEBOTS_HOME /usr/local/webots
ENV LD_LIBRARY_PATH $WEBOTS_HOME/lib/controller:$LD_LIBRARY_PATH


ADD requirements.txt .
# Install python dependencies
RUN pip install -r requirements.txt

RUN if [ $branch = "dev" ]; then pip install -i https://test.pypi.org/simple/ deepbots ; else pip install deepbots ; fi

RUN pip install 'ray[tune]' 'ray[rllib]'

# Fix the error of the custome enviroment on Ray
ADD preprocessors.py .
RUN cp -r preprocessors.py opt/conda/lib/python3.8/site-packages/ray/rllib/models/
RUN rm preprocessors.py


WORKDIR /workspace
RUN chmod -R a+w /workspace