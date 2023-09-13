#base image
# Base image
FROM python:3.8

# Switch to application directory
WORKDIR /app

# Update image os
RUN apt-get update

# Install Miniconda
RUN curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o Miniconda3-latest-Linux-x86_64.sh && \
    chmod +x Miniconda3-latest-Linux-x86_64.sh && \
    sh Miniconda3-latest-Linux-x86_64.sh -b && \
    rm Miniconda3-latest-Linux-x86_64.sh

# Set environment variables
ENV PATH="/root/miniconda3/bin:${PATH}"

# Create and activate conda environment
RUN conda create --name tf python=3.8.18 -y
RUN echo "conda activate tf" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

# Install CUDA Toolkit and cuDNN (assuming NVIDIA GPU support)
RUN conda install -c conda-forge cudatoolkit==11.8.0 -y
RUN pip install nvidia-cudnn-cu11==8.6.0.163

RUN pip install --upgrade pip

RUN curl -o Miniconda3-latest-Linux-x86_64.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

RUN conda install -c conda-forge cudatoolkit=11.8.0 -y 

RUN pip install nvidia-cudnn-cu11==8.6.0.163 -y

RUN mkdir -p $CONDA_PREFIX/etc/conda/activate.d
RUN echo 'CUDNN_PATH=$(dirname $(python -c "import nvidia.cudnn;print(nvidia.cudnn.__file__)"))' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
RUN echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CUDNN_PATH/lib:$CONDA_PREFIX/lib/' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh

# Install CUDA Toolkit and cuDNN (assuming NVIDIA GPU support)
RUN conda install -c conda-forge cudatoolkit==11.8.0 -y

RUN pip install nvidia-cudnn-cu11==8.6.0.163

RUN wget https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow-2.13.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

RUN chmod +x tensorflow-2.13.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl -y

RUN pip install tensorflow-2.13.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl -y

RUN rm tensorflow-2.13.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
# -----------------------------------
# environment variables
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./ /app/

# -----------------------------------
# run the app (re-configure port if necessary)
EXPOSE 5000

CMD ["python", "Main.py"]