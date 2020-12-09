FROM centos:8
LABEL creator.name="Avi Layani"
LABEL creator.mail="alayani@redhat.com"
LABEL version="0.1"
LABEL release-date="Dec-09-2020"
RUN yum -y install python3 golang git --nodocs
RUN pip3 install elasticsearch

RUN git clone https://github.com/shinexia/elasticsearch-dump.git
RUN cd elasticsearch-dump ; go build
WORKDIR /elasticsearch-dump 
COPY *.py /elasticsearch-dump/
ENTRYPOINT /bin/bash

