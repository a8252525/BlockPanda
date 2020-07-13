set_local_testnet(){
    cd
    git clone https://github.com/Intelligent-Systems-Lab/EOS-lab-testnet.git
    echo -ne '\n' | bash EOS-lab-testnet/quick_start_multi.sh
}


read -p "Press [Enter] set start local testnet..."
sleep 1
set_local_testnet