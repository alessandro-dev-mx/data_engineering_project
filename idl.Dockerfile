FROM centos

RUN cd /etc/yum.repos.d/ && \
    sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-* && \
    sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*

# Install base utilities
RUN yum update -y && \
    yum install -y wget && \
    yum clean packages && \
    rm -rf /var/lib/apt/lists/*

# Install miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
     /bin/bash ~/miniconda.sh -b -p /opt/conda

# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH

# Set work directory
WORKDIR /idl

# Copy local code and assets to the workdir
ADD python python
ADD resources resources

# Create conda environment
RUN conda create -n idl_env python=3.8 -y && \
    /opt/conda/bin/activate idl_env 
RUN pip install -r /idl/python/requirements.txt 

ENTRYPOINT [ "python", "/idl/python/load_data.py" ]
