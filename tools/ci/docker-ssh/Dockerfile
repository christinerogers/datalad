FROM neurodebian:latest
MAINTAINER DataLad developers

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y --no-install-recommends eatmydata
RUN eatmydata apt-get install -y --no-install-recommends gnupg locales
RUN echo "en_US.UTF-8 UTF-8" >>/etc/locale.gen
RUN locale-gen

RUN eatmydata apt-get install -y --no-install-recommends \
    git git-annex-standalone datalad p7zip

RUN eatmydata apt-get install -y --no-install-recommends openssh-server
RUN mkdir -p /var/run/sshd

RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN useradd -ms /bin/bash notdl
RUN chown -R notdl:notdl /home/notdl/
RUN echo 'notdl:notdl' | chpasswd

ARG UID=1000

RUN useradd -ms /bin/bash -ou $UID dl
RUN mkdir -p /home/dl/.ssh
RUN chown -R dl:dl /home/dl/
RUN echo 'dl:dl' | chpasswd

RUN git config --system user.name "Docker Datalad"
RUN git config --system user.email "docker-datalad@example.com"

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
