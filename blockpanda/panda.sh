#!/bin/bash

cleos wallet unlock --password PW5JAAqDnfrN56bHxsYeci94RSwARcqrLeSUimvKFmrejRw5n13Lm
eosio-cpp blockpanda.cpp -o blockpanda.wasm
cleos set contract blockpanda ../blockpanda/ -p blockpanda@active
echo "cleos push action blockpanda upsert "
cleos push action blockpanda c2r '["123123", "bob", ""]' -p bob@active
#cleos push action blockpanda upsert2 '["bob", "no panda here"]' -p bob@active
cleos get table blockpanda blockpanda people

#cleos push action addressbook erase '["123123"]' -p bob@active