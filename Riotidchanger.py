from Rengar import Rengar
import json

rengar = Rengar()


def change_riotid():
	name = input("Type the new name\n")
	tag = input("Type the new tag\n")

	body = {
	f"gameName": name,
	"tagLine": tag
	}

	change = rengar.lcu_request("POST", "/lol-summoner/v1/save-alias", body)
	print(change.text)
	input("\nPress Enter.")
