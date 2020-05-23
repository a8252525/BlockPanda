#include <eosio/eosio.hpp>
#include <eosio/system.hpp>

using namespace eosio;

// This will bind the contract to 'blockpanda' account
//class [[eosio::contract("blockpanda")]] blockpanda : public eosio::contract {
class [[eosio::contract]] blockpanda : public eosio::contract {

public:

  blockpanda(name receiver, name code,  datastream<const char*> ds): contract(receiver, code, ds) {}

  [[eosio::action]]
  void c2r(uint64_t txid, name customer, std::string temp_cus, std::string time_c) {
    require_auth( customer );
    temp_index addresses( get_self(), get_first_receiver().value );
    auto iterator = addresses.find(txid);
    if( iterator == addresses.end() )
    {
      addresses.emplace(customer, [&]( auto& row ) {
       row.txid = txid;
       row.customer = customer;
       row.temp_cus = temp_cus;
       row.time_c = time_c;
      });
    }

  }

  [[eosio::action]]
  void rc2rw(uint64_t txid, name r_cook, std::string temp_rc, std::string time_rc) {
    require_auth( r_cook );
    temp_index addresses( get_self(), get_first_receiver().value );
    auto iterator = addresses.find(txid);

      addresses.modify(iterator, r_cook, [&]( auto& row ) {
       row.r_cook = r_cook;
       row.temp_rc = temp_rc;
       row.time_rc = time_rc;
      });
  }

  [[eosio::action]]
  void rw2de(uint64_t txid, name r_w, std::string temp_rw, std::string time_rw) {
    require_auth( r_w );
    temp_index addresses( get_self(), get_first_receiver().value );
    auto iterator = addresses.find(txid);

      addresses.modify(iterator, r_w, [&]( auto& row ) {
       row.r_w = r_w;
       row.temp_rw = temp_rw;
       row.time_rw = time_rw;
      });
  }

  [[eosio::action]]
  void de2c(uint64_t txid, name de, std::string temp_de, std::string time_de) {
    require_auth( de );
    temp_index addresses( get_self(), get_first_receiver().value );
    auto iterator = addresses.find(txid);

      addresses.modify(iterator, de, [&]( auto& row ) {
       row.de = de;
       row.temp_de = temp_de;
       row.time_de = time_de;
      });
  }  

  [[eosio::action]]
  void erase(uint64_t txid) {
    //require_auth(txid);

    temp_index addresses( get_self(), get_first_receiver().value);

    auto iterator = addresses.find(txid);
    check(iterator != addresses.end(), "Record does not exist");
    addresses.erase(iterator);
  }

private:
  struct [[eosio::table]] person {
     uint64_t txid;
     name customer;
     std::string temp_cus;
     std::string time_c;
     name r_cook;
     std::string temp_rc;
     std::string time_rc;
     name r_w;
     std::string temp_rw;
     std::string time_rw;
     name de;
     std::string temp_de;
     std::string time_de;

    uint64_t primary_key() const { return txid; }
  };
  typedef eosio::multi_index<"people"_n, person> temp_index;

};    

//name format : https://github.com/EOSIO/eos/issues/2699#issuecomment-385853668

