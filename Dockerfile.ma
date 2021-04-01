ARG ARCH=
FROM ${ARCH}fedora
LABEL creator.name="Avi Layani"
LABEL creator.mail="alayani@redhat.com"
LABEL version="0.2"
LABEL release-date="Jan-06-2021"
RUN echo "%_netsharedpath /sys:/proc" >> /etc/rpm/macros.dist
RUN yum update -y
RUN yum -y install python3 golang git --nodocs
RUN pip3 install elasticsearch

RUN git clone https://github.com/shinexia/elasticsearch-dump.git
RUN cd elasticsearch-dump ; go build
WORKDIR /elasticsearch-dump 
COPY *.py /elasticsearch-dump/
ENTRYPOINT /bin/bash

