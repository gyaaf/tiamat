# Standard library imports
import threading
from os import system

# Third-party imports
from termcolor import colored

# Local imports
from Icons import change_profile_icon
from Backgrounds import change_background
from Reveal import reveal
from AutoAccept import autoaccept
from Dodge import dodge
from Riotidchanger import change_riotid
from Iconsclient import icon_client
from RestartUX import restart
from Rengar import check_league_client
from InstalockAutoban import InstalockAutoban
from disconnect_reconnect_chat import Chat


class MenuOption:
    """Representa uma opção do menu com seu título e função associada."""

    def __init__(self, title, action, show_state=False, feature_name=""):
        self.title = title
        self.action = action
        self.show_state = show_state
        self.feature_name = feature_name


class LeagueClientTool:
    """Classe principal que gerencia todas as funcionalidades do cliente."""

    ASCII_ART = """
    ▄▄▄█████▓ ██▓ ▄▄▄       ███▄ ▄███▓ ▄▄▄     ▄▄▄█████▓
    ▓  ██▒ ▓▒▓██▒▒████▄    ▓██▒▀█▀ ██▒▒████▄   ▓  ██▒ ▓▒
    ▒ ▓██░ ▒░▒██▒▒██  ▀█▄  ▓██    ▓██░▒██  ▀█▄ ▒ ▓██░ ▒░
    ░ ▓██▓ ░ ░██░░██▄▄▄▄██ ▒██    ▒██ ░██▄▄▄▄██░ ▓██▓ ░ 
      ▒██▒ ░ ░██░ ▓█   ▓██▒▒██▒   ░██▒ ▓█   ▓██▒ ▒██▒ ░ 
      ▒ ░░   ░▓   ▒▒   ▓▒█░░ ▒░   ░  ░ ▒▒   ▓▒█░ ▒ ░░   
        ░     ▒ ░  ▒   ▒▒ ░░  ░      ░  ▒   ▒▒ ░   ░    
      ░       ▒ ░  ░   ▒   ░      ░     ░   ▒    ░      
              ░        ░  ░       ░         ░  ░        
    """

    def __init__(self):
        self.auto_accept = autoaccept()
        self.instalock_autoban = InstalockAutoban()
        self.chat = Chat()
        self._initialize_menu_options()
        self._initialize_threads()

    def _initialize_menu_options(self):
        """Inicializa as opções do menu."""
        self.menu_options = {
            1: MenuOption("Icon Changer", change_profile_icon),
            2: MenuOption("Client-Only Icon Changer", icon_client),
            3: MenuOption("Background Changer", change_background),
            4: MenuOption("Lobby Reveal", reveal),
            5: MenuOption("Toggle Auto Accept", self.auto_accept.toggle_auto_accept, True, "auto_accept"),
            6: MenuOption("Dodge", dodge),
            7: MenuOption("Riot ID Changer", change_riotid),
            8: MenuOption("Restart Client UX", restart),
            9: MenuOption("Toggle Instalock", self.instalock_autoban.toggle_instalock, True, "instalock"),
            10: MenuOption("Toggle AutoBan", self.instalock_autoban.toggle_auto_ban, True, "autoban"),
            11: MenuOption("Disconnect Chat", self.chat.toggle_chat, True, "chat"),
            99: MenuOption("Exit", self._exit_program)
        }

    def _initialize_threads(self):
        """Inicializa as threads necessárias."""
        threading.Thread(
            target=self.auto_accept.monitor_queue,
            daemon=True
        ).start()

        threading.Thread(
            target=self.instalock_autoban.monitor_champ_select,
            daemon=True
        ).start()

    def _display_menu(self):
        """Exibe o menu principal com estados atualizados."""
        system("cls")
        print(colored(self.ASCII_ART, "magenta"))
        print("\n")

        for key, option in self.menu_options.items():
            menu_text = f"{key}. {option.title}"

            if option.show_state:
                if key == 9:  # Instalock
                    state = "ON" if self.instalock_autoban.instalock_enabled else "OFF"
                    menu_text += f" ({colored(state, 'yellow')}) - Champion: {colored(self.instalock_autoban.instalock_champion, 'cyan')}"
                elif key == 10:  # AutoBan
                    state = "ON" if self.instalock_autoban.auto_ban_enabled else "OFF"
                    menu_text += f" ({colored(state, 'yellow')}) - Champion: {colored(self.instalock_autoban.auto_ban_champion, 'cyan')}"
                elif key == 11:
                    state = "ON" if self.chat.chat_state else "OFF"
                    menu_text += f" ({colored(state, 'yellow')})"
                else:
                    state = self._get_feature_state(option.feature_name)
                    menu_text += f" ({colored(state, 'yellow')})"

            print(menu_text)

        return int(input("\n~-> "))

    def _get_feature_state(self, feature_name):
        """Retorna o estado atual de uma feature."""
        states = {
            "auto_accept": self.auto_accept.auto_accept_enabled,
            "chat": self.chat.return_state()
        }
        return "ON" if states.get(feature_name, False) else "OFF"

    def _handle_champion_selection(self, option):
        """Gerencia a seleção de campeões para Instalock/AutoBan."""
        champion_name = input("Enter the champion name (or 99 to disable): ")
        if option == 9:
            self.instalock_autoban.set_instalock_champion(champion_name)
        else:
            self.instalock_autoban.set_auto_ban_champion(champion_name)

    def _exit_program(self):
        """Encerra o programa de forma limpa."""
        raise KeyboardInterrupt

    def run(self):
        """Loop principal do programa."""
        print("\nWaiting for league client.\n")
        check_league_client()

        while True:
            try:
                check_league_client()
                option = self._display_menu()

                if option not in self.menu_options:
                    continue

                if option in [9, 10]:
                    self._handle_champion_selection(option)
                else:
                    self.menu_options[option].action()

            except KeyboardInterrupt:
                self._exit_program()
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                continue


if __name__ == "__main__":
    client_tool = LeagueClientTool()
    client_tool.run()