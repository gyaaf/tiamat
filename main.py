from Icons import change_profile_icon
from Backgrounds import change_background
from Reveal import reveal
from termcolor import colored
from AutoAccept import autoaccept
from Dodge import dodge
from Riotidchanger import change_riotid


import threading
from os import system

def intro():
    print(colored("""
    ▄▄▄█████▓ ██▓ ▄▄▄       ███▄ ▄███▓ ▄▄▄     ▄▄▄█████▓
    ▓  ██▒ ▓▒▓██▒▒████▄    ▓██▒▀█▀ ██▒▒████▄   ▓  ██▒ ▓▒
    ▒ ▓██░ ▒░▒██▒▒██  ▀█▄  ▓██    ▓██░▒██  ▀█▄ ▒ ▓██░ ▒░
    ░ ▓██▓ ░ ░██░░██▄▄▄▄██ ▒██    ▒██ ░██▄▄▄▄██░ ▓██▓ ░ 
      ▒██▒ ░ ░██░ ▓█   ▓██▒▒██▒   ░██▒ ▓█   ▓██▒ ▒██▒ ░ 
      ▒ ░░   ░▓   ▒▒   ▓▒█░░ ▒░   ░  ░ ▒▒   ▓▒█░ ▒ ░░   
        ░     ▒ ░  ▒   ▒▒ ░░  ░      ░  ▒   ▒▒ ░   ░    
      ░       ▒ ░  ░   ▒   ░      ░     ░   ▒    ░      
              ░        ░  ░       ░         ░  ░        
        """, "magenta"))

def exit_program():
    exit()

def main_menu():
    auto_accept = autoaccept()

    options = {
        1: change_profile_icon,
        2: change_background,
        3: reveal,
        4: auto_accept.toggle_auto_accept,
        5: dodge,
        6: change_riotid,
        99: exit_program,
    }

    # Inicia a thread para aceitar partidas automaticamente
    threading.Thread(target=auto_accept.auto_accept_matches, daemon=True).start()

    while True:
        try:
            system("cls")
            intro()
            # Atualiza o estado do Auto Accept no menu dinamicamente
            auto_accept_state = "ON" if auto_accept.auto_accept_enabled else "OFF"

            # Exibe o menu com o estado do Auto Accept atualizado
            option = int(input(f"""
1. Icon Changer
2. Background Changer
3. Lobby Reveal
4. Toggle Auto Accept ({colored(auto_accept_state, "yellow")})
5. Dodge
6. Riot ID Changer

99. Exit\n
~-> """))

            if option in options:
                options[option]()  # Chama a função correspondente
            else:
                print("Invalid option. Please choose a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main_menu()
