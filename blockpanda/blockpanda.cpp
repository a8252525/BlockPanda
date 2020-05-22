#include <eosio/eosio.hpp>

using namespace eosio;

// This will bind the contract to 'blockpanda' account
//class [[eosio::contract("blockpanda")]] blockpanda : public eosio::contract {
class [[eosio::contract]] blockpanda : public eosio::contract {

public:

  blockpanda(name receiver, name code,  datastream<const char*> ds): contract(receiver, code, ds) {}

  [[eosio::action]]
  void c2r(name txid, name customer, std::string temp_cus) {
    require_auth( customer );
    temp_index addresses( get_self(), get_first_receiver().value );
    auto iterator = addresses.find(txid.value);
    if( iterator == addresses.end() )
    {
      addresses.emplace(customer, [&]( auto& row ) {
       row.txid = txid;
       row.customer = customer;
       row.temp_cus = temp_cus;
      //  row.street = street;
      //  row.city = city;
      //  row.state = state;
      });
    }
  //   else {
  //     addresses.modify(iterator, user, [&]( auto& row ) {
  //       row.key = user;
  //       row.first_name = first_name;
  //       row.last_name = last_name;
  //       row.street = street;
  //       row.city = city;
  //       row.state = state;
  //     });
  //   }
  }

  [[eosio::action]]
  void rc2rw(name txid, name r_cook, std::string temp_rc) {
    require_auth( r_cook );
    temp_index addresses( get_self(), get_first_receiver().value );
    auto iterator = addresses.find(txid.value);

      addresses.modify(iterator, r_cook, [&]( auto& row ) {
       row.r_cook = r_cook;
       row.temp_rc = temp_rc; 
      });
  }
  
  [[eosio::action]]
  void erase(name txid) {
    //require_auth(txid);

    temp_index addresses( get_self(), get_first_receiver().value);

    auto iterator = addresses.find(txid.value);
    check(iterator != addresses.end(), "Record does not exist");
    addresses.erase(iterator);
  }

private:
  struct [[eosio::table]] person {
     name txid;
     name customer;
     std::string temp_cus;
     name r_cook;
     std::string temp_rc;
    //  std::string city;
    //  std::string state;
    uint64_t primary_key() const { return txid.value; }
  };
  typedef eosio::multi_index<"people"_n, person> temp_index;

};    

//name format : https://github.com/EOSIO/eos/issues/2699#issuecomment-385853668
