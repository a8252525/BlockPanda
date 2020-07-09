

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
    cd ..
    rm -r df_temp
fi


