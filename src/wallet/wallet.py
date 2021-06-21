from hashlib import sha256
from datetime import datetime
from uuid import getnode as get_mac


from util.util import get_random_string
from util.constant import FULL_WALLET_PATH
from util.serialize import write_to_file, read_from_file
from chain.block.transaction import Transaction

# TODO Asymmetric Encryption and Decryption in file
# using two keys - a private key and a public key.

class Wallet:
	id = 1

	def __init__(self, password, wallet = None):
		if wallet == None:
			self.id = Wallet.id
			
			self.wallet_id:str = self.create_wallet_id()
			self.password:str = self.hash(password)

			self.secret_key = self.hash(self.wallet_id + self.password)

			Wallet.id += 1 # not part of constructor but get from blockchain same as balance
		else:
			w = self.load_wallet()
			self.id = w.id
			self.wallet_id = w.wallet_id
			self.password = w.password
			self.secret_key = w.secret_key



	def create_wallet_id(self) -> str:
		mac = str(get_mac())
		t = str(datetime.timestamp(datetime.utcnow()))
		t = '1621685424.04008'
		#temp = str(get_random_string(32)) +	str(datetime.timestamp(datetime.utcnow()))
		return self.hash(mac+t)
		
	def hash(self, data) -> str:
		return sha256(data.encode()).hexdigest()

	def validate_access(self, wallet_id, password):
		if self.wallet_id == wallet_id and self.password == self.hash(password): return True
		else: return False
	
	def encrypt(self): #verschlüsseln
		pass
	def decrypt(self): #entschlüsseln
		pass

	def write_wallet_to_file(self):
		FULL_WALLET_PATH.touch(exist_ok=True) # create file if noch exists
		write_to_file(path=FULL_WALLET_PATH, obj=self)

	def write_wallet_to_blockchain(self) -> Transaction:
		transaction = Transaction(type = 2, created_by = self.wallet_id, amount=0)
		return transaction

	def init_wallet_to_blockchain(self) -> Transaction:
		transaction = Transaction(type = 3, created_by = '0'*64 , recipient=self.wallet_id, amount=10)
		return transaction

	def send_transaction(self, recipient='send to',data='approved', amount=1):
		transaction = Transaction(type=3, 
			created_by =self.wallet_id, 
			recipient=recipient, 
			data=data,
			amount=amount)
		return transaction

	@staticmethod
	def load_wallet():
		if FULL_WALLET_PATH.stat().st_size > 0: 
			wallet = read_from_file(path=FULL_WALLET_PATH)
			return wallet

#w = Wallet(password='test')

#w = Wallet(password='test', wallet=Wallet.load_wallet())

#print(w.id, w.wallet_id, w.password, w.secret_key)

#print(w.validate_access(
#	wallet_id='78275f08ae4c369b3bb8340686d0833bf726a643bc6c0a80f9c6b9fa2b89dda9',
#	password='test'))

#w.write_wallet_to_file()
