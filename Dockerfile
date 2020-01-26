FROM python:3.7-alpine

COPY src/config.py /src/
COPY src/sendSMS.py /src/
COPY src/twitterScrape.py /src/
COPY requirements.txt /tmp
COPY contacts.ini /src/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /src
CMD ["python3", "twitterScrape.py"]