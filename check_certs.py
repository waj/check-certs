import ssl
import socket
import sys
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import datetime

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

for host in sys.stdin:
  host = host.strip()
  try:
    with socket.create_connection((host, 443), 1) as sock:
      with context.wrap_socket(sock, server_hostname=host) as ssock:
        cert_der = ssock.getpeercert(binary_form=True)
        cert = x509.load_der_x509_certificate(cert_der, default_backend())

        issuer = cert.issuer.rfc4514_string()
        subject = cert.subject.rfc4514_string()
        exp = cert.not_valid_after
        exp_in = exp - datetime.datetime.now()
        print('%s,"%s","%s",%d,' % (host, issuer, subject, exp_in.days))
  except KeyboardInterrupt:
    break
  except:
    print('%s,,,,%s' % (host, sys.exc_info()[1]))
