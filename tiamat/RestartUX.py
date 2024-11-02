from Rengar import Rengar

rengar = Rengar()

def restart():

	rengar.lcu_request("POST", '/riotclient/kill-and-restart-ux','')
