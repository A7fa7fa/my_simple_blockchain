import pickle


def write_to_file(path, obj ):

	with open(path, "wb") as file:
		pickled_blockchain = pickle.dumps(obj)
		file.write(pickled_blockchain)

def read_from_file(path):

	with open(path, "rb") as file:
		pickled =  file.read()
		obj = pickle.loads(pickled)
	return obj

