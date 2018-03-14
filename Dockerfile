FROM		scholzj/centos-builder-base:centos7-latest
MAINTAINER 	JAkub Scholz "www@scholzj.com"

ARG FTP_USERNAME
ARG FTP_PASSWORD
ARG FTP_HOSTNAME

USER root

# Create the RPMs
RUN rpmdev-setuptree
WORKDIR /root/rpmbuild/SOURCES

RUN wget https://github.com/apache/qpid-python/archive/master.tar.gz
RUN tar -xf master.tar.gz
RUN mv qpid-python-master/ qpid-python-1.38.0/
RUN tar -z -cf qpid-python-1.38.0.tar.gz qpid-python-1.38.0/
RUN rm -rf master.tar.gz qpid-python-1.38.0/

ADD ./qpid-python.spec /root/rpmbuild/SPECS/qpid-python.spec

WORKDIR /root/rpmbuild/SPECS
RUN rpmbuild -ba qpid-python.spec

# Create and deploy the RPMs to the repository
RUN mkdir -p /root/repo/CentOS/7/x86_64
RUN mkdir -p /root/repo/CentOS/7/SRPMS
RUN mv /root/rpmbuild/RPMS/x86_64/*.rpm /root/repo/CentOS/7/x86_64/
RUN mv /root/rpmbuild/SRPMS/*.rpm /root/repo/CentOS/7/SRPMS/
WORKDIR /root/repo/CentOS/7/x86_64/
RUN createrepo .
WORKDIR /root/repo/CentOS/7/SRPMS
RUN createrepo .
RUN ncftpget -u $FTP_USERNAME -p $FTP_PASSWORD -R -DD $FTP_HOSTNAME /tmp/ /web/repo/qpid-python-devel/
RUN ncftpput -u $FTP_USERNAME -p $FTP_PASSWORD -R $FTP_HOSTNAME /web/repo/qpid-python-devel/ /root/repo/*

# Nothing to run
CMD    /bin/bash
