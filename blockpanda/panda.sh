#!/bin/bash

cleos wallet unlock --password $(cat wallet_pass.txt)
eosio-cpp blockpanda.cpp -o blockpanda.wasm
echo "Setting contract"
cleos set contract blockpanda ../blockpanda/ -p blockpanda@active
echo "cleos push action blockpanda c2r "
cleos push action blockpanda c2r '["123123", "bob", "36.7"]' -p bob@active
echo "cleos push action blockpanda rc2rw"

cleos push action blockpanda rc2rw '["123123", "cook", "35"]' -p cook@active

cleos push action blockpanda rw2de '["123123", "waiter", "35.5"]' -p waiter@active

cleos push action blockpanda de2c '["123123", "delivery", "38"]' -p delivery@active

echo "get table back"
cleos get table blockpanda blockpanda people

#cleos push action blockpanda erase '["123123"]' -p bob@active

