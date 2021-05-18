# %%

import time
import threading
from datetime import datetime


from chain.blockchain import Blockchain

blockchain = Blockchain(zero_lenght=3, block_length = 2)

exitFlag = 0


class Miner(threading.Thread):
# solves hash
# competes with other miner in network

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.found_hash = False

    def run(self):
        print('start hash')
        while exitFlag == 0:
            if not(blockchain.get_last_block().is_block_free()):
                if self.found_hash == False:
                    if (blockchain.get_last_block().calculate_valid_hash()):
                        self.found_hash = True
                        blockchain.add_new_block()
                        print(datetime.utcnow(), threading.current_thread().name, 'Found Hash')
            else:
                self.found_hash = False
                time.sleep(2)


class Wallet(threading.Thread):
# can send transactions to other wallets

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print('start write tran')
        while exitFlag == 0:
            if blockchain.get_transaction_queue_lenght() > 0:
                blockchain.write_transaction()
            else:
                time.sleep(2)

class Network(threading.Thread):
# provides P2P networking and adresses to other nodes in network
# discover and and maintain connection to peers
# mandatory for all nodes to validate and propagate transactions and blocks
    pass

class Blockchain(threading.Thread): 
# stores full blockchain
    pass

def main():
    

    miner = Miner(1, 'miner')
    wallet = Wallet(2, 'wallet')

    miner.start()
    wallet.start()


    for i in range(200):
        blockchain.add_transaction(i)
        #time.sleep(0.1)

    for i in range(200):
        #print(blockchain.get_last_block().__repr__())
        time.sleep(2)

if __name__ == "__main__":
    main()



# %%
