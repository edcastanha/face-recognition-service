FROM nvcr.io/nvidia/tensorflow:23.08-tf2-py3

# environment variables
ENV PYTHONUNBUFFERED=1

EXPOSE 6000

WORKDIR /app

RUN mkdir /app/capturas/

RUN mkdir /app/ftp/

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6 -y

COPY ./task/ /app/

RUN pip install -e ./lib/

RUN pip install -r requirements.txt

RUN rm -rf /tmp/*

CMD ["python", "consumer-extrair-faces-files.py" ]
