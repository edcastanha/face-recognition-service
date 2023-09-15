FROM nvcr.io/nvidia/tensorflow:23.08-tf2-py3

# environment variables
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./lib/ /app/lib/

COPY ./publicar.py /app/
COPY ./consumer-extrair-faces-files.py /app/

RUN mkdir /app/capturas/

RUN mkdir /app/ftp/

COPY ./requirements.txt /app/

RUN pip install -e ./lib/

RUN pip install -r requirements.txt

CMD ["python", "consumer-extrair-faces-files.py" ]
