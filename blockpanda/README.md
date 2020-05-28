# Blockpanda smart contract
Just like the flow in the ***panda.sh.***
You have to unlock the wallet of your own wallet.
Remember to save the wallet key in the **wallet.txt.**(You won't upload the key to github since we has written wallet.txt  to the .gitignore. Don't worry.)
```
cleos wallet unlock --password $(cat wallet_pass.txt)
```
And we also need to *compile* the smart contract with the command below.
```
eosio-cpp blockpanda.cpp -o blockpanda.wasm
```
After the smart contract being compiled, we will need to *deploy* the contract to the smart contract.
```
cleos set contract "account" "contract_dir/blockpanda" -p "account"@active
```
Remember to create the account.
Now we have set the contract to the account.

Let's push the action now.
```
cleos push action "account you deploy the contract" "action" '["transaction ID", "account", "temperature of account", "time of  uploading"]' -p "account"@active
```
The account in the json(inside []) need to be the same as the one you use the permission(the account after the -p).
There are four action, **c2r, rc2rw, rw2de and de2c**, in this blockpanda contract. 
We get wired action name here since the number of action name need to be less than 12.

#### action
**c2r**: when customer upload the information contain the temperature of his own. This action will cause when customer send an order to the restaurant.

**rc2rw**: Send the action when the cook pass the stuff to the waiters. Upload with the temperature of the cook.

**rw2de**: Send this action when waiters give the stuff to the delivery man. Upload the temperature of the waiter.

**de2c**: Send this action when delivery man give the stuff to the customer. Upload the temperature of the delivery man. We don't need the temperature of customer since we have it in the c2r action.

*You have to push action of c2r first in order to create the space. Otherwise, you won't be bale to push the action.*

After all the data uploading, we need to get it back with **"get table"**
```
cleos get table "account you deploy the contract" "scope: also be the account you deploy the contract" people
```
The **scope** of all the action in this blockpanda contract are all set to be the account you deploy the contract. 
You can management the scope of getting table, but we didn't set it. If you want to know more about the "scope", you can learn some information [here](https://eosio.stackexchange.com/questions/3534/scope-in-the-get-table-command) and [eosio.token](https://github.com/EOSIO/eosio.contracts/tree/master/contracts/eosio.token)

*people* is the table name we define in the smart contract.

## get table
Finally, you get the information like this
```
{
"rows": [{
"txid": "123123",
"customer": "bob",
"temp_cus": "36.7",
"time_c": "12:30:31",
"r_cook": "cook",
"temp_rc": "35",
"time_rc": "12:30:31",
"r_w": "waiter",
"temp_rw": "35.5",
"time_rw": "12:30:31",
"de": "delivery man",
"temp_de": "38",
"time_de": "12:30:31"
}
],
"more": false,
"next_key": ""
}
```
You may not see the whole table when you upload more than 10 different transaction ID.
If you get "more":true in the end, you get more information in the table. You just can't see it.
Add "-l -1" after the command and you can see the whole table. 

Like this:
```
cleos get table "account you deploy the contract" "scope: also the account you deploy the contract" people -l -1
```

