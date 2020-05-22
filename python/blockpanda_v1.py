from eospy.cleos import Cleos

ce = Cleos(url='https://api.testnet.eos.io')
info = ce.get_info()

print(info)

head = info['head_block_num']
print('Head Block number is', head)