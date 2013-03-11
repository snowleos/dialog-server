class DataMinerError(Exception):
	'''Data miner exceptions base class'''
	pass

class DataSourceNotReachableException(DataMinerError):
	'''Data source is not reachable'''
	pass

class DataNotFoundException(DataMinerError):
	'''Did not found any information'''
	pass

class NoSuchMinerException(DataMinerError):
	'''No such miner defined'''
	pass