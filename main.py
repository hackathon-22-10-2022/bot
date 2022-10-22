from config import config



def hello():
	print(config.get_mongo_client())


	


if __name__ == "__main__":
	hello()

