FROM python:3

RUN pip install cryptography
ADD check_certs.py /check_certs.py

CMD ["python3", "-u", "/check_certs.py"]