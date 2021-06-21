from hashlib import sha256
from datetime import datetime
import json

from util.decorator import timer
from util.constant import BLOCK_LENGTH, DIFFICULTY_TARGET, VERSION
from util.decorator import timer

# TODO Merkle Tree / Root

class Block(object):
	
	def __init__(self, index, previous_block_hash):
		self.version:int = int(VERSION)
		self.index:int = int(index)
		self.timestamp:datetime.timestamp = datetime.timestamp(datetime.utcnow())
		self.end_timestamp:datetime.timestamp = datetime.timestamp(datetime.utcnow()) # not used do calc this blocks hash. to display/debug time to live
		self.prev_block_hash:str = previous_block_hash
		self.hash:str = '' # not used do calc this blocks hash. added after calculation
		self.nonce:int = 0
		self.hashed_by = ''
		self.transactions:list = []

	def write_transaction_to_block(self, transaction):
		self.transactions.append(transaction)

	def is_block_closed(self) -> bool:
		return self.transactions[-1].is_closing_transaction()

	def set_hashed_by(self, hashed_by):
		self.hashed_by = hashed_by
	
	def get_hashed_by(self) -> str:
		return self.hashed_by

	def is_hash_valid(self) -> str:
		return (self.hash.startswith('0' * int(DIFFICULTY_TARGET)))

	@timer
	def calculate_valid_hash(self):
		print('start hashing')
		while True:
			self.hash = self.calculate_hash()
			if self.is_hash_valid():
				break
			else:
				self.nonce += 1

	def calculate_hash(self) -> str:
		temp = self.to_string()
		return sha256(temp.encode()).hexdigest()

	def to_string(self) -> str:
		str_tuple = (str(self.version),
					str(self.index),
					str(self.get_transactions_json()),
					str(self.timestamp),
					str(self.prev_block_hash),
					str(self.nonce),
					str(self.hashed_by))
		block_string = "".join(str_tuple)
		return block_string

	def __repr__(self) -> str:
		return "{} - {} - {} - {} - {} - {} - {} - {}".format(
			str(self.index),
			str(self.get_transactions_json()), 
			self.timestamp, 
			self.end_timestamp,
			self.prev_block_hash, 
			self.hash,
			self.nonce,
			self.hashed_by)

	def is_block_free(self) -> bool:
		if self.get_amount_of_transactions() < BLOCK_LENGTH: return True
		else: False

	def get_transactions__json(self) -> json:
		return self.get_json()

	def get_amount_of_transactions(self) -> int:
		return len(self.transactions)

	def get_created_at(self) -> datetime:
		return self.timestamp
	
	def get_transactions_json(self) -> json:
		t = []
		for transaction in self.transactions:
			t.append(transaction.get_json())
		return t
		
	def is_block_valid(self) -> bool:        
		return self.is_hash_valid(self.calculate_hash())

