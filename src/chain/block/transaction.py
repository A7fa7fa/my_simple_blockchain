import json
from datetime import datetime

class Transaction(object):
	
	id = 0

	# type
	# 0 = closing block
	# 1 = random
	# 2 = wallet creation
	# 3 = send
	# 4 = new ballance #TODO
	# 5 = mining reward
	
	def __init__(self, type=1, created_by = '0'*64, 
				recipient='0'*64, data='', amount = '') -> None:
		self.id = Transaction.id
		self.timestamp = datetime.timestamp(datetime.utcnow())
		self.type = type
		self.created_by = created_by
		self.recipient = recipient
		self.data = data
		self.amount = amount
		Transaction.id += 1

	def get_type(self) -> int:
		return self.type 
	
	def is_closing_transaction(self) -> bool:
		return self.get_type() == 0

	def get_dict(self) -> dict:
		return (self.__dict__)

	def get_json(self) -> json:
		return json.dumps(self.get_dict())
