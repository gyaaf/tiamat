from Icons import change_profile_icon
from Backgrounds import change_background
from Reveal import reveal
from termcolor import colored
from AutoAccept import autoaccept
from Dodge import dodge
from Riotidchanger import change_riotid
from Iconsclient import icon_client
from RestartUX import restart
from Welcome import welcome
from Rengar import check_league_client



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
        2: icon_client,
        3: change_background,
        4: reveal,
        5: auto_accept.toggle_auto_accept,
        6: dodge,
        7: change_riotid,
        8: restart,
        99: exit_program,
    }

    # Inicia a thread para aceitar partidas automaticamente
    threading.Thread(target=auto_accept.auto_accept_matches, daemon=True).start()

    while True:
        try:
            print("\nWaiting for league client.\n")
            check_league_client()
            system("cls")
            intro()
            print("\n")
            welcome()
            # Atualiza o estado do Auto Accept no menu dinamicamente
            auto_accept_state = "ON" if auto_accept.auto_accept_enabled else "OFF"

            # Exibe o menu com o estado do Auto Accept atualizado
            option = int(input(f"""
1. Icon Changer
2. Client-Only Icon Changer
3. Background Changer
4. Lobby Reveal
5. Toggle Auto Accept ({colored(auto_accept_state, "yellow")})
6. Dodge
7. Riot ID Changer
8. Restart Client UX

99. Exit\n
~-> """))

            if option in options:
                options[option]()  # Chama a função correspondente
            else:
                print("Invalid option. Please choose a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyError:
            print("Option not found.")

if __name__ == "__main__":
    main_menu()
