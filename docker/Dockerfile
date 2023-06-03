FROM cyberbotics/webots:latest

ARG branch
ARG conda

# Install Ubuntu libraries
RUN apt-get update && \
    apt-get install -y git pip apt-utils

# Install miniconda
SHELL ["/bin/bash", "-c"]
RUN if [[ -z "$conda" ]]; then echo build without conda ;\
    else\
        wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
        /bin/bash ~/miniconda.sh -b -p /opt/conda ; fi
SHELL ["/bin/bash", "-c"]
ENV PATH=${conda:+/opt/conda/bin}:$PATH

# Install deepbots
RUN python3 -m pip install --upgrade pip
RUN pip install --upgrade pip
RUN pip install gym==0.21.0
RUN if [ $branch = "main" ]; then pip install deepbots ; \
    else \
        if [ $branch = "dev" ]; then \
            pip install git+https://github.com/aidudezzz/deepbots.git ; \
        else if [[ $branch == *"deepbots"* ]]; then \
            pip install --index-url https://pypi.org/simple/ $branch ; \
            fi ; \
        fi ; \
    fi

WORKDIR /workspace
RUN chmod -R a+w /workspace
