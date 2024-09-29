from Rengar import Rengar

rengar = Rengar()


def welcome():
	req = rengar.lcu_request("GET", "/lol-summoner/v1/current-summoner", "").json()

	name = req["gameName"]

	return name


