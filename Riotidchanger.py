from Rengar import Rengar
import json

rengar = Rengar()


def change_riotid():
	name = input("Type the new name\n")
	tag = input("Type the new tag\n")

	if tag == "":

		print("Insert a valid tag.")
		input("\nPress Enter.")

	else:
		body = {
		f"gameName": name,
		"tagLine": tag
		}

		change = rengar.lcu_request("POST", "/lol-summoner/v1/save-alias", body)
		print(change.text)
		input("\nPress Enter.")
