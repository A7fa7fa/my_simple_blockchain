from os import write
import threading
from datetime import datetime
import time
from pathlib import Path

from chain.blockchain import Blockchain
from chain.block.transaction import Transaction
from util.serialize import read_from_file
from util.constant import FULL_BLOCKCHAIN_PATH
from util.util import get_random_string
from wallet.wallet import Wallet

def main():
	
	FULL_BLOCKCHAIN_PATH.touch(exist_ok=True) # create file if noch exists
	
	if FULL_BLOCKCHAIN_PATH.stat().st_size > 0: 
		blockchain = Blockchain(blockchain=read_from_file(path = FULL_BLOCKCHAIN_PATH))
		# check if blockchain is_valid
	else:
		blockchain = Blockchain()

	# check existing chain - and load  - hdd or remote
	# get last block and confirm it is the one to hash
	# start hashing
	# check if hash is broken
	# until me or someone breaks the hash
	# get next block and confirm it is the one to hash
	# start all over
	

	# calcuate hash/miner
	hash = threading.Thread(target=blockchain.calculate_valid_hash_of_last_block, name='hash')

	# adding transactions to blocks
	transaction = threading.Thread(target=blockchain.write_transaction, name='transa')

	# provides P2P networking and adresses to other nodes in network
	# discover and and maintain connection to peers
	# mandatory for all nodes to validate and propagate transactions and blocks
	networking = ''

	# handels personal wallet
	# wallet = Wallet(password='test')
	wallet = Wallet(password='test', wallet=Wallet.load_wallet())

	# wallet.write_wallet_to_file()
	blockchain.add_transaction(wallet.write_wallet_to_blockchain())
	blockchain.add_transaction(wallet.init_wallet_to_blockchain())

	

	# print(w.id, w.wallet_id, w.password, w.secret_key)
	# 1 78275f08ae4c369b3bb8340686d0833bf726a643bc6c0a80f9c6b9fa2b89dda9 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08 aa304a869b5d1f843df111776a4053ceeab0947e8fa1ce1ac13a3a5df155c4aa
	# stores full blockchain
	
	full_node = ''
	for i in range(5):
		blockchain.add_randome_transaction(created_by = wallet.wallet_id, transaction=get_random_string(32))


	while True:
		if not(blockchain.get_last_block().is_block_free()) and not(blockchain.get_last_block().is_hash_valid()) and blockchain.get_last_block().is_block_closed():
			if hash.is_alive() == False:
				try:
					blockchain.get_last_block().set_hashed_by(hashed_by=wallet.wallet_id)
					hash = threading.Thread(target=blockchain.calculate_valid_hash_of_last_block, name='hash')
					#print('start hash')
					hash.start()
				except Exception as e:
					print(f'hash {e}')

		if blockchain.get_last_block().is_hash_valid():
			# safe blockchain to file
			blockchain.serialize_blockchain()
			
			# reward miner
			blockchain.reward_miner()
			print(blockchain.get_last_block().__repr__())
			# init new block
			blockchain.add_new_block()

		if blockchain.get_transaction_queue_lenght() >= 3 and blockchain.get_last_block().index > 0 and blockchain.get_last_block().is_block_free():
			if transaction.is_alive() == False:
				try:
					transaction = threading.Thread(target=blockchain.write_transaction, name='transa')
					#print('add transaction to block')
					transaction.start()
				except Exception as e:
					print(f'trans {e}')

		send_trans = wallet.send_transaction(recipient='send to',data='approved', amount=1)
		if (blockchain.validate_transaction(send_trans)): blockchain.add_transaction(send_trans)

		#blockchain.add_randome_transaction(created_by = wallet.wallet_id, transaction=get_random_string(32))

		#for thread in threading.enumerate(): 
		#	print(thread.name)
		#print(threading.current_thread().name, blockchain.get_last_block().index, blockchain.get_last_block().prev_block_hash, blockchain.get_last_block().hash, blockchain.get_last_block().nonce, blockchain.get_last_block().get_amount_of_transactions())

if __name__ == "__main__":
	main()

