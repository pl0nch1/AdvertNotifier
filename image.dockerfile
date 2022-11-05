FROM python:3.9
COPY /app app
RUN apt-get update
RUN apt-get install -y chromium libglib2.0 libnss3 libgconf-2-4 libfontconfig1
RUN pip install -r app/requirements.txt
# CMD ./app/avito_driver.py