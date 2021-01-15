FROM python:3.9.1-slim-buster
WORKDIR /the/workdir/path
ADD main.py /
RUN pip install websockets
RUN pip install dataclasses
ENV KEY=ENV
ENV TIME_URL=ENV
ENV URL=ENV
CMD ["python", "./main.py"]
