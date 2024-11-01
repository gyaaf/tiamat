# Importing all client tools
from Icons import change_profile_icon
from Backgrounds import change_background
from Reveal import reveal
from termcolor import colored
from AutoAccept import autoaccept
from Dodge import dodge
from Riotidchanger import change_riotid
from Iconsclient import icon_client
from RestartUX import restart
from Rengar import check_league_client
from InstalockAutoban import InstalockAutoban  # Importando o novo módulo
import threading
from os import system


# Defining core script functions

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
    raise KeyboardInterrupt


def main_menu():
    print("\nWaiting for league client.\n")
    check_league_client()

    auto_accept = autoaccept()
    instalock_autoban = InstalockAutoban()  # Instanciando o novo módulo

    options = {
        1: change_profile_icon,
        2: icon_client,
        3: change_background,
        4: reveal,
        5: auto_accept.toggle_auto_accept,
        6: dodge,
        7: change_riotid,
        8: restart,
        9: instalock_autoban.toggle_instalock,  # Alterna manualmente o Instalock
        10: instalock_autoban.toggle_auto_ban,  # Alterna manualmente o AutoBan
        99: exit_program,
    }

    # Inicia a thread para aceitar partidas automaticamente
    threading.Thread(target=auto_accept.monitor_queue, daemon=True).start()

    # Inicia a thread para monitorar a seleção de campeões e aplicar Instalock e AutoBan
    threading.Thread(target=instalock_autoban.monitor_champ_select, daemon=True).start()

    while True:
        try:
            check_league_client()
            system("cls")
            intro()
            print("\n")
            # Atualiza os estados de auto accept, instalock e autoban
            auto_accept_state = "ON" if auto_accept.auto_accept_enabled else "OFF"
            instalock_state = "ON" if instalock_autoban.instalock_enabled else "OFF"
            autoban_state = "ON" if instalock_autoban.auto_ban_enabled else "OFF"

            # Menu principal com estados
            option = int(input(f"""
1. Icon Changer
2. Client-Only Icon Changer
3. Background Changer
4. Lobby Reveal
5. Toggle Auto Accept ({colored(auto_accept_state, "yellow")})
6. Dodge
7. Riot ID Changer
8. Restart Client UX
9. Toggle Autopick ({colored(instalock_state, "yellow")}) - Champion: {colored(instalock_autoban.instalock_champion, "cyan")}
10. Toggle AutoBan ({colored(autoban_state, "yellow")}) - Champion: {colored(instalock_autoban.auto_ban_champion, "cyan")}

99. Exit\n 
~-> """))

            if option in options:
                if option == 9 or option == 10:
                    # Pergunta o nome do campeão ao usuário para Instalock ou AutoBan
                    champion_name = input("Enter the champion name (or 99 to disable): ")
                    if option == 9:
                        instalock_autoban.set_instalock_champion(champion_name)  # Definir campeão ativa o Instalock
                    elif option == 10:
                        instalock_autoban.set_auto_ban_champion(champion_name)  # Definir campeão ativa o AutoBan
                else:
                    options[option]()  # Chama a função correta para outros casos
            else:
                continue


        except KeyboardInterrupt:
            exit_program()
        except:
            pass


if __name__ == "__main__":
    main_menu()
