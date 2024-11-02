import json
from termcolor import colored
from Rengar import Rengar  # Certifique-se de que o Rengar.py está no mesmo diretório

def change_profile_icon():
    # Inicializa a classe Rengar
    rengar = Rengar()

    # Pede o ID do ícone ao usuário
    icon_id = input(colored("Type the icon ID (1 - 100): \n", "magenta"))

    # Verifica se o input é um número válido
    try:
        icon_id = int(icon_id)
    except ValueError:
        print("Please insert a valid number.")
        return

    # Cria o corpo da requisição
    body = {"profileIconId": icon_id}

    # Faz a requisição PUT usando a classe Rengar
    try:
        response = rengar.lcu_request("PUT", "/lol-summoner/v1/current-summoner/icon", body)
        if response.status_code == 201 or response.status_code == 200:
            print(colored(f"Icon sucessfully changed to {icon_id}", "green"))
        else:
            print(f"Error: {response.status_code}")
            print(f"Details: {response.text}")
            input("\nPress Enter.")
    except Exception as e:
        print(f"Error on sending the request: {e}")
        input("\nPress Enter.")



if __name__ == "__main__":
	change_profile_icon()
