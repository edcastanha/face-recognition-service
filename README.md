


# PREPARACAO de AMBIENTE::

nvidia-smi

conda install -c conda-forge cudatoolkit=11.8.0
pip install nvidia-cudnn-cu11==8.6.0.163

mkdir -p $CONDA_PREFIX/etc/conda/activate.d
echo 'CUDNN_PATH=$(dirname $(python -c "import nvidia.cudnn;print(nvidia.cudnn.__file__)"))' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CUDNN_PATH/lib:$CONDA_PREFIX/lib/' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh

pip install --upgrade pip

pip install tensorflow==2.13.*

py -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"


### Suporte a GPU Python 3.8	
https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow-2.13.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

## REQUIREMENTS