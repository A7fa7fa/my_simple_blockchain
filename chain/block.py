from hashlib import sha256
from datetime import datetime
from util.decorator import timer


class Block(object):
    def __init__(self,index, previous_block_hash, zero_lenght):
        self.index = index
        self.timestamp = datetime.utcnow()
        self.end_timestamp = datetime.utcnow() # not used do calc this blocks hash. to display/debug time to live
        self.prev_block_hash = previous_block_hash
        self.hash = '' # not used do calc this blocks hash. added after calculation
        self.nonce = 0
        self.zero_lenght = zero_lenght
        self.transactions = []

    def write_transaction(self, transaction):
        self.transactions.append(transaction)

    def is_hash_valid(self, hash) -> str:
        return (hash.startswith('0' * self.zero_lenght))

    def calculate_valid_hash(self):
        if not(self.is_hash_valid(self.hash)):
            self.hash = self.calculate_hash()
            self.nonce += 1
            return False
        else:
            self.nonce -= 1
            self.end_timestamp = datetime.utcnow()
            return True

    def calculate_hash(self) -> str:
        temp = self.to_string()
        return sha256(temp.encode()).hexdigest()

    def to_string(self) -> str:
        return "{}{}{}{}{}".format(
            str(self.index),
            str(self.transactions), 
            self.timestamp, 
            self.prev_block_hash, 
            self.nonce)

    def __repr__(self) -> str:
        return "{} - {} - {} - {} - {} - {} - {}".format(
            str(self.index),
            str(self.transactions), 
            self.timestamp, 
            self.end_timestamp,
            self.prev_block_hash, 
            self.hash,
            self.nonce)

    def is_block_free(self) -> bool:
        if self.get_amount_of_transactions() < 3: return True
        else: False

    def get_amount_of_transactions(self) -> int:
        return len(self.transactions)
    
    def is_block_valid(self):        
        return self.is_hash_valid(self.calculate_hash())

