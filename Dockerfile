FROM centos:8

# Install pre-requsit
RUN yum -y install python3 golang git --nodocs 
#USER 1000
RUN pip3 install elasticsearch 
#RUN yum -y install epel-release --nodocs
#RUN yum --enablerepo=epel -y install sshpass
#RUN yum -y install openssh-clients --nodocs

# Hammercli
# epel-release is needed, but was installed above.
#RUN yum install -y https://yum.theforeman.org/releases/2.1/el8/x86_64/foreman-release.rpm
#RUN yum install -y https://yum.theforeman.org/releases/2.1/el8/x86_64/rubygem-hammer_cli-2.1.0-1.el8.noarch.rpm 
#RUN yum install -y http://yum.theforeman.org/releases/2.1/el8/x86_64/rubygem-hammer_cli_foreman-2.1.0-2.el8.noarch.rpm
#
#RUN yum install -y rubygem-hammer_cli \
#	rubygem-hammer_cli_foreman

#RUN pip3 install j2cli

RUN git clone https://github.com/shinexia/elasticsearch-dump.git
RUN cd elasticsearch-dump ; go build
WORKDIR /elasticsearch-dump 
COPY elasticsearch.py /elasticsearch-dump/

#RUN pip3 install -r requirements.txt


# Done. Now run it.
ENTRYPOINT /bin/bash

