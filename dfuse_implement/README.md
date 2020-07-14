# BlockPanda with dfuse

## build docker 

```shell=
cd [to docker folder]

docker build -t eos_lab:dfuse .
```  

```shell=
docker run -d -it -p 8180:8080/tcp -p 8181:8081/tcp -p 18080:18080/tcp --name eos_dfuse eos_lab:dfuse
```

code-server will launch at port 18080.

Go to http://localhost:18080

pass=eospc

## install

```shell=
git clone https://github.com/a8252525/BlockPanda.git
cd BlockPanda && git checkout dfuse
```

```shell=
cd dfuse_implement

bash install.sh
```

## launch local testnet

```shell=
bash launch_local_testnet.sh

echo "Create snapshot~"
echo "This might take about 3 min"
curl -X POST http://127.0.0.1:8800/v1/producer/create_snapshot
```

## use dfuse example

```shell=
cd
mkdir dfexp && cd dfexp

dfuseeos init --skip-checks

> ? Do you want dfuse for EOSIO to run a producing node for you? [y/N] N
> First peer to connect: 127.0.0.1:9001█
> Add another peer? (leave blank to skip): 127.0.0.1:9002█
> Add another peer? (leave blank to skip):

cp ../nodes/node0000/genesis.json  ./mindreader
```


## kill & restart testnet

```shell=
cd && rm -r account_200.txt config.ini eosio-wallet nodeos.log nodes wallet_pass.txt

cd BlockPanda/dfuse_implement
bash launch_local_testnet.sh
```
cd BlockPanda/dfuse_implement
bash launch_local_testnet.sh
