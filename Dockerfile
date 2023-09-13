#base image
FROM python:3.8
# -----------------------------------
# switch to application directory
WORKDIR /app
# -----------------------------------
# create required folder
#RUN mkdir /app
# -----------------------------------
# Copy required files from repo into image

COPY ./ /app/

RUN ["curl","https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o Miniconda3-latest-Linux-x86_64.sh"]

RUN Miniconda3-latest-Linux-x86_64.sh
# -----------------------------------
# update image os
RUN apt-get update

RUN ["conda"," create"," --name"," tf"," python=3.8.18"]

RUN conda deactivate

RUN conda activate tf

RUN pip install cudatoolkit=11.2
# -----------------------------------
# environment variables
ENV PYTHONUNBUFFERED=1

# -----------------------------------
# run the app (re-configure port if necessary)
EXPOSE 5000

CMD ["python", "Main.py"]
