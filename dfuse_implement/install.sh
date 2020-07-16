

echo '██████╗ ██╗      ██████╗  ██████╗██╗  ██╗██████╗  █████╗ ███╗   ██╗██████╗  █████╗ '
echo '██╔══██╗██║     ██╔═══██╗██╔════╝██║ ██╔╝██╔══██╗██╔══██╗████╗  ██║██╔══██╗██╔══██╗'
echo '██████╔╝██║     ██║   ██║██║     █████╔╝ ██████╔╝███████║██╔██╗ ██║██║  ██║███████║'
echo '██╔══██╗██║     ██║   ██║██║     ██╔═██╗ ██╔═══╝ ██╔══██║██║╚██╗██║██║  ██║██╔══██║'
echo '██████╔╝███████╗╚██████╔╝╚██████╗██║  ██╗██║     ██║  ██║██║ ╚████║██████╔╝██║  ██║'
echo '╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝'

# Download [dfuse-eosio_0.1.0-beta4_linux_x86_64.tar.gz] from github.
cd
FILE_SOURCE=https://github.com/dfuse-io/dfuse-eosio/releases/download/v0.1.0-beta4/dfuse-eosio_0.1.0-beta4_linux_x86_64.tar.gz
FILE=/usr/local/bin/dfuseeos
if [ -f "$FILE" ]; then
    echo "$FILE exists."
else 
    echo "$FILE does not exist."
    echo ''
    mkdir df_temp
    cd df_temp
    wget $FILE_SOURCE
    tar_file=`echo $FILE_SOURCE | rev | cut -d'/' -f 1 | rev`
    echo $tar_file
    tar zxvf $tar_file
    mv ./dfuseeos /usr/local/bin
    
    wget https://github.com/dfuse-io/eos/releases/download/v2.0.6-dm-12.0/eosio_2.0.6-dm.12.0-1-ubuntu-18.04_amd64.deb
    apt -y install ./eosio_2.0.6-dm.12.0-1-ubuntu-18.04_amd64.deb
    cd ..
    rm -r df_temp
fi


echo 
echo "Install nodejs and go."
echo

apt -y install curl dirmngr apt-transport-https lsb-release ca-certificates
curl -sL https://deb.nodesource.com/setup_12.x |  bash
apt-get install -y nodejs

npm install -g npm

cd /tmp
wget https://dl.google.com/go/go1.11.linux-amd64.tar.gz
tar -xvf go1.11.linux-amd64.tar.gz
mv go /usr/local
cd