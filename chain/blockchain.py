from block import Block
from datetime import datetime
import time
import threading

class Blockchain(object):

    def __init__(self, zero_lenght = 3, block_length = 2):
        self.chain:Block = []
        self.transaction_queue = []
        self.zero_lenght = int(zero_lenght)
        self.block_length = int(block_length)
        self.set_genesis_block()

        print(datetime.utcnow(), threading.current_thread().name, 'zero_lenght', zero_lenght, 'block_length', block_length)
    
    def set_genesis_block(self):
        self.transaction_queue.append("Genesis")
        prev_hash = '0'*64
        genesis_block = Block(len(self.chain), prev_hash, self.zero_lenght)
        self.chain.append(genesis_block)
        self.write_transaction()
        self.chain[-1].calculate_valid_hash()
        self.add_new_block()
    
    def get_last_hash(self) -> str:
        last_hash = self.get_last_block().hash
        return (last_hash)

    def add_transaction(self, tansaction):
        self.transaction_queue.append(tansaction)

    def get_transaction_queue_lenght(self) -> int:
        return len(self.transaction_queue)

    def write_transaction(self):
        if self.chain[-1].is_block_free():
            print(datetime.utcnow(), threading.current_thread().name, 'wrote trancaction to block', self.get_last_block().index)
            self.chain[-1].write_transaction(self.transaction_queue.pop(0))

    def add_new_block(self):
        prev_hash = self.get_last_hash()
        new_block = Block(len(self.chain), prev_hash, self.zero_lenght)
        self.chain.append(new_block)
        print(self.chain[-2].__repr__())

    def get_blocks(self) -> list :
        return (self.chain)
    
    def get_last_block(self) -> Block:
        return (self.chain[-1])
        
    def get_fist_block(self) -> Block:
        return (self.chain[0])

    def to_string(self):
        for block in self.get_blocks():
            print(block.__repr__())

    # for debugging purpose
    def is_chain_valid(self):
        for block in self.get_blocks():
            print(block.to_string(), block.is_block_valid())


