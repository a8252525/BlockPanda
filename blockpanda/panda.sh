cleos wallet unlock --password PW5JAAqDnfrN56bHxsYeci94RSwARcqrLeSUimvKFmrejRw5n13Lm
eosio-cpp blockpanda.cpp -o blockpanda.wasm
cleos set contract blockpanda ../blockpanda/ -p blockpanda@active
cleos push action blockpanda upsert '["bob", "bob"]' -p bob@active
cleos push action blockpanda upsert2 '["bob", "pppppanda"]' -p bob@active
cleos get table blockpanda blockpanda people