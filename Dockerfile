#base image
FROM python:3.8
# -----------------------------------
# switch to application directory

RUN ["curl","https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o Miniconda3-latest-Linux-x86_64.sh"]

RUN Miniconda3-latest-Linux-x86_64.sh
# -----------------------------------
# update image os
RUN apt-get update

RUN ["conda"," create"," --name"," tf"," python=3.8.18"]

RUN conda deactivate

RUN conda activate tf

RUN ["conda"," create"," --name"," tf"," python=3.8.18"]

RUN conda deactivate

RUN conda activate tf

RUN pip install --upgrade pip

RUN curl -o Miniconda3-latest-Linux-x86_64.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

RUN sh Miniconda3-latest-Linux-x86_64.sh

RUN rm ~/Miniconda3-latest-Linux-x86_64.sh

RUN conda create --name tf python=3.8.18 -y

RUN conda deactivate

RUN conda activate tf

RUN conda install -c conda-forge cudatoolkit=11.8.0 -y 

RUN pip install nvidia-cudnn-cu11==8.6.0.163 -y

RUN mkdir -p $CONDA_PREFIX/etc/conda/activate.d
RUN echo 'CUDNN_PATH=$(dirname $(python -c "import nvidia.cudnn;print(nvidia.cudnn.__file__)"))' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
RUN echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CUDNN_PATH/lib:$CONDA_PREFIX/lib/' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh


RUN wget https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow-2.13.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

RUN pip install tensorflow-2.13.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl -y

RUN rm ~/tensorflow-2.13.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
# -----------------------------------
# environment variables
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./ /app/

# -----------------------------------
# run the app (re-configure port if necessary)
EXPOSE 5000

CMD ["python", "Main.py"]
