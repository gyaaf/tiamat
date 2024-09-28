from Rengar import Rengar

rengar = Rengar()


def welcome():
	req = rengar.lcu_request("GET", "/lol-chat/v1/me", "").json()

	name = req["gameName"]

	print(f"Welcome {name}")


