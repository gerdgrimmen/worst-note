FROM python:3.13

WORKDIR /usr/local/app

COPY ./main.py main.py
COPY ./api_data_structure.json api_data.json
COPY ./index.html index.html

EXPOSE 5000

RUN useradd worst
USER worst

CMD ["python", "main.py"]