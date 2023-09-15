FROM nvcr.io/nvidia/tensorflow:23.08-tf2-py3

# environment variables
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN mkdir /app/capturas/

RUN mkdir /app/ftp/

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6 -y

COPY ./lib/ /app/lib/

COPY ./publicar.py /app/

COPY ./consumer-extrair-faces-files.py /app/

COPY ./requirements.txt /app/

RUN pip install -e ./lib/

RUN pip install -r requirements.txt

RUN rm -rf /tmp/*


#CMD ["python", "consumer-extrair-faces-files.py" ]
