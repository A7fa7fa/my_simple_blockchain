from datetime import datetime
from os import write
import time
import threading

from util.constant import DIFFICULTY_TARGET, BLOCK_LENGTH, FULL_BLOCKCHAIN_PATH, MINING_REWARD
from chain.block.block import Block
from chain.block.transaction import Transaction
from util.serialize import write_to_file

class Blockchain(object):

	def __init__(self, blockchain = None):
		if blockchain == None:
			self.chain:Block = []
			self.transaction_queue = []
			self.set_genesis_block()

		else:
			self.chain = blockchain.chain
			self.transaction_queue = blockchain.transaction_queue

		print(datetime.utcnow(), threading.current_thread().name, 
			'DIFFICULTY_TARGET', DIFFICULTY_TARGET, 
			'BLOCK_LENGTH', BLOCK_LENGTH)
		
	
	def set_genesis_block(self):
		self.transaction_queue.append(Transaction(data="Genesis"))
		prev_hash = '0'*64
		genesis_block = Block(len(self.chain), prev_hash)
		genesis_block.set_hashed_by(hashed_by = '0'*64)
		self.chain.append(genesis_block)
		self.chain[-1].write_transaction_to_block(self.transaction_queue.pop(0))
		self.chain[-1].calculate_valid_hash()
	
	def get_last_hash(self) -> str:
		last_hash = self.get_last_block().hash
		return (last_hash)

	def add_randome_transaction(self, created_by,  transaction):
		self.transaction_queue.append(Transaction(type = 1, created_by=created_by,data=transaction))

	def add_transaction(self,  transaction):
		self.transaction_queue.append(transaction)

	def close_block(self):
		data = 'block closed'
		self.get_last_block().write_transaction_to_block(Transaction(type=0, data=data))

	def get_transaction_queue_lenght(self) -> int:
		return len(self.transaction_queue)

	def validate_transaction(self, transaction):
		ballance = 0
		for block in self.chain:
			ballance += self.iterate_over_transactions(ballance = ballance, transactions=block.transactions, transaction=transaction)
			ballance += self.iterate_over_transactions(ballance = ballance, transactions=self.transaction_queue, transaction=transaction)
		if (int(ballance) - int(transaction.amount)) <= 0: return False
		else: True
		#create new transaction with new account ballance
		# so just find transaction with last account ballance
	
	def iterate_over_transactions(self, ballance, transactions, transaction) -> int:
		for trans in transactions:
			if trans.created_by == transaction.created_by:
				if trans.type == 0: pass
				elif trans.type == 1: pass
				elif trans.type == 2: ballance += int(trans.amount)
				elif trans.type == 3: ballance -= int(trans.amount)
				elif trans.type == 4: pass
				elif trans.type == 5: pass
			if trans.recipient == transaction.created_by:
				if trans.type == 0: pass
				elif trans.type == 1: pass
				elif trans.type == 2: pass
				elif trans.type == 3: ballance += int(trans.amount)
				elif trans.type == 4: pass
				elif trans.type == 5: ballance += int(trans.amount)
				ballance += int(trans.amount)
		return ballance

	def write_transaction(self):
		#print('start writing transaction')
		while True:
			if self.get_last_block().is_block_free():
				#print(datetime.utcnow(), threading.current_thread().name, 'wrote trancaction to block', self.get_last_block().index)
				self.get_last_block().write_transaction_to_block(self.transaction_queue.pop(0))
			else:
				self.close_block()
				break
		#print('finished writing transactions')

	def add_new_block(self):
		prev_hash = self.get_last_hash()
		new_block = Block(len(self.chain), prev_hash)
		self.chain.append(new_block)
		

	def get_blocks(self) -> list :
		return (self.chain)
	
	def get_last_block(self) -> Block:
		return (self.chain[-1])
		
	def get_fist_block(self) -> Block:
		return (self.chain[0])

	def to_string(self):
		for block in self.get_blocks():
			print(block.__repr__())

	def calculate_valid_hash_of_last_block(self):
		self.get_last_block().calculate_valid_hash()

	def reward_miner(self):
		self.add_transaction(Transaction(type=5, created_by = '0'*64,recipient=self.get_last_block().get_hashed_by(), data='', amount = MINING_REWARD))


	# for debugging purpose
	def is_chain_valid(self):
		for block in self.get_blocks():
			#print(block.to_string(), block.is_block_valid())
			print(block.is_block_valid())


	def serialize_blockchain(self):
		write_to_file(path = FULL_BLOCKCHAIN_PATH, obj = self)

		
