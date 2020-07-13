FROM ubuntu:18.04
  
RUN apt-get update && apt-get install -y openssh-server


RUN apt-get update && apt-get -y upgrade &&\
    apt-get install -y apt-utils openssh-server software-properties-common &&\
    apt-get install -y autotools-dev automake curl git wget zip build-essential gcc pkg-config net-tools nano &&\
    apt-get install -y python3 python3-pip

#RUN pip3 install numpy 

#RUN apt-get install -y gdb

#RUN mkdir /var/run/sshd
RUN echo 'root:eospc' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config &&\
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
  
# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
  
ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

RUN service ssh restart
  
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]

#ENV eos_path=/root/eos_build
#RUN mkdir -p $eos_path

# install cmake 3.12.0
RUN wget https://github.com/Kitware/CMake/releases/download/v3.12.0/cmake-3.12.0.tar.gz &&\
    tar zxvf cmake-3.12.0.tar.gz &&\
    cd cmake-3.12.0 &&\
    ./bootstrap &&\
    make -j8 &&\
    make install &&\
    cd / &&\
    rm -r cmake-3.12.0.tar.gz cmake-3.12.0 &&\
    cmake --version

RUN cd &&\
    wget https://github.com/EOSIO/eos/releases/download/v2.0.5/eosio_2.0.5-1-ubuntu-18.04_amd64.deb &&\
    apt -y install ./eosio_2.0.5-1-ubuntu-18.04_amd64.deb &&\
    rm -r eosio_2.0.5-1-ubuntu-18.04_amd64.deb
    #wget https://github.com/EOSIO/eosio.cdt/releases/download/v1.6.1/eosio.cdt_1.6.1-1_amd64.deb &&\
    #apt -y install ./eosio.cdt_1.6.1-1_amd64.deb

# RUN cd &&\
#     wget https://github.com/EOSIO/eosio.cdt/releases/download/v1.7.0/eosio.cdt_1.7.0-1-ubuntu-18.04_amd64.deb &&\
#     apt -y install ./eosio.cdt_1.7.0-1-ubuntu-18.04_amd64.deb &&\
#     rm -r eosio.cdt_1.7.0-1-ubuntu-18.04_amd64.deb

RUN cd &&\
    wget https://github.com/eosio/eosio.cdt/releases/download/v1.6.3/eosio.cdt_1.6.3-1-ubuntu-18.04_amd64.deb &&\
    wget https://github.com/EOSIO/eosio.cdt/releases/download/v1.7.0/eosio.cdt_1.7.0-1-ubuntu-18.04_amd64.deb
    

RUN cd  &&\
    apt -y install ./eosio.cdt_1.6.3-1-ubuntu-18.04_amd64.deb


RUN cd &&\
    git clone https://github.com/EOSIO/eosio.contracts.git eosio.contracts-1.8.x &&\
    cd ./eosio.contracts-1.8.x/ &&\
    git checkout v1.8.0 &&\
    ./build.sh -y &&\
    cd ./build/contracts/ &&\
    echo "EOSIO_OLD_CONTRACTS_DIRECTORY=$(pwd)" >> ~/.bashrc

ENV EOSIO_OLD_CONTRACTS_DIRECTORY=$(pwd)

RUN cd &&\
    apt -y install ./eosio.cdt_1.7.0-1-ubuntu-18.04_amd64.deb

RUN cd &&\
    git clone https://github.com/EOSIO/eosio.contracts.git &&\
    cd ./eosio.contracts/ &&\
    git checkout release/1.9.x &&\
    ./build.sh -y &&\
    cd ./build/contracts/ &&\
    echo "EOSIO_CONTRACTS_DIRECTORY=$(pwd)" >> ~/.bashrc

ENV EOSIO_CONTRACTS_DIRECTORY=$(pwd)

RUN cd &&\
    rm eosio.cdt_1.6.3-1-ubuntu-18.04_amd64.deb eosio.cdt_1.7.0-1-ubuntu-18.04_amd64.deb

# install nodejs 10
RUN cd && apt -y install curl dirmngr apt-transport-https lsb-release ca-certificates &&\
    apt-get install -y nodejs &&\
    curl -sL https://deb.nodesource.com/setup_10.x | bash &&\
    apt-get install -y nodejs

# https://github.com/cdr/code-serve
EXPOSE 18080
ENV PASSWORD=eospc

RUN apt install curl &&\
    wget https://github.com/cdr/code-server/releases/download/v3.3.1/code-server-3.3.1-linux-amd64.tar.gz && \
    tar zxvf code-server-3.3.1-linux-amd64.tar.gz && \
    rm -r code-server-3.3.1-linux-amd64.tar.gz

#https://github.com/ml-tooling/ml-workspace/blob/develop/Dockerfile#L930
RUN \
    # Make zsh the default shell
    chsh -s $(which bash) root

# setting code-server default to bash and resize font
RUN mkdir -p /root/.local/share/code-server/User &&\
    touch /root/.local/share/code-server/User/settings.json &&\
    echo '{"editor.fontSize": 18,"terminal.integrated.fontSize": 16,"terminal.integrated.shell.linux": "/bin/bash",}' >> /root/.local/share/code-server/User/settings.json &&\
    echo 'export PS1="\[\e[32m\][\[\e[m\]\[\e[31m\]\u\[\e[m\]\[\e[33m\]@\[\e[m\]\[\e[32m\]\h\[\e[m\]:\[\e[36m\]\w\[\e[m\]\[\e[32m\]]\[\e[m\]\[\e[32;47m\]\\$\[\e[m\] "' >> /root/.bashrc
# run code server   
ENTRYPOINT ./code-server-3.3.1-linux-amd64/bin/code-server --host 0.0.0.0  --port 18080 >> codeserver.txt
