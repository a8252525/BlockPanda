#!/bin/bash

cleos wallet unlock --password PW5J7aqcuSyZCc2oDy34mYmZFgGhchJgyFdmM39Zoib6hn63BXPXY
eosio-cpp blockpanda.cpp -o blockpanda.wasm
echo "Setting contract"
cleos set contract blockpanda ../blockpanda/ -p blockpanda@active
echo "cleos push action blockpanda c2r "
cleos push action blockpanda c2r '["123123", "bob", "36.7"]' -p bob@active
echo "cleos push action blockpanda rc2rw"

cleos push action blockpanda rc2rw '["123123", "cook", "35"]' -p cook@active

echo "get table back"
cleos get table blockpanda blockpanda people

#cleos push action blockpanda erase '["123123"]' -p bob@active
