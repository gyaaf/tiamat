import threading
import time
import random
from Rengar import Rengar


class InstalockAutoban:
    def __init__(self):
        self.champ_dict = {}  # Moved from ChampionConverter
        self.instalock_enabled = False
        self.instalock_champion = "Random"
        self.auto_ban_enabled = False
        self.auto_ban_champion = "None"
        self.rengar = Rengar()  # Instância da classe Rengar para fazer requisições
        self.update_champion_list()  # Initialize champion list on startup

    def update_champion_list(self):
        """
        Atualiza a lista de campeões obtendo seus IDs e nomes da API LCU.
        """
        #print("Fetching champion list from LCU...")
        response = self.rengar.lcu_request("GET", "/lol-champ-select/v1/all-grid-champions", "")

        if response.status_code == 200:
            champion_data = response.json()
            for champ in champion_data:
                champ_id = champ["id"]
                champ_name = champ["name"]
                self.champ_dict[champ_name.lower()] = champ_id  # Armazena o nome em minúsculas para fácil busca
            #print("Champion list updated successfully.")
        else:
            print("Failed to fetch champion data.")

    def champ_name_to_id(self, champ_name):
        """
        Converte o nome de um campeão para o ID correspondente.
        Se o campeão não for encontrado, retorna -1.
        """
        champ_name = champ_name.lower()  # Normaliza o nome do campeão para minúsculas
        return self.champ_dict.get(champ_name, -1)  # Retorna o ID do campeão ou -1 se não encontrado

    def set_instalock_champion(self, champion_name):
        if champion_name == "99":
            self.instalock_enabled = False
            self.instalock_champion = "None"
        else:
            champ_id = self.champ_name_to_id(champion_name)
            if champ_id == -1:
                print(f"Champion '{champion_name}' not found.")
            else:
                self.instalock_champion = champion_name
                self.instalock_enabled = True

    def set_auto_ban_champion(self, champion_name):
        if champion_name == "99":
            self.auto_ban_enabled = False
            self.auto_ban_champion = "None"
        else:
            champ_id = self.champ_name_to_id(champion_name)
            if champ_id == -1:
                print(f"Champion '{champion_name}' not found.")
            else:
                self.auto_ban_champion = champion_name
                self.auto_ban_enabled = True

    def monitor_champ_select(self):
        """
        Monitora continuamente o estado da seleção de campeões e executa
        Instalock ou AutoBan quando apropriado.
        """
        while True:
            try:
                champ_select_resp = self.rengar.lcu_request("GET", "/lol-champ-select/v1/session", "")
                if "RPC_ERROR" not in champ_select_resp.text:
                    root_champ_select = champ_select_resp.json()
                    cell_id = root_champ_select.get("localPlayerCellId")

                    if cell_id == None:
                        time.sleep(0.3)
                        continue

                    for actions in root_champ_select["actions"]:
                        if not isinstance(actions, list):
                            continue
                        for action in actions:
                            if self.instalock_enabled and action["actorCellId"] == cell_id and action[
                                "type"] == "pick" and not action["completed"]:
                                time.sleep(0.3)

                                if self.instalock_champion == "Random":
                                    instalock_champs = list(
                                        self.champ_dict.items())  # Convert dictionary items to list of tuples
                                    champion_id = random.choice(instalock_champs)[
                                        1]  # Get the ID from the randomly chosen tuple
                                else:
                                    champion_id = self.champ_name_to_id(self.instalock_champion)

                                patch_resp = self.rengar.lcu_request(
                                    "PATCH",
                                    f"/lol-champ-select/v1/session/actions/{action['id']}",
                                    {"completed": True, "championId": champion_id}
                                )

                                time.sleep(0.3)

                            elif self.auto_ban_enabled and action["actorCellId"] == cell_id and action[
                                "type"] == "ban" and not action["completed"]:
                                time.sleep(0.3)
                                champion_id = self.champ_name_to_id(self.auto_ban_champion)

                                patch_resp = self.rengar.lcu_request(
                                    "PATCH",
                                    f"/lol-champ-select/v1/session/actions/{action['id']}",
                                    {"completed": True, "championId": champion_id}
                                )

                                continue

                                time.sleep(0.3)

                time.sleep(0.3)
            except:
                pass

    def toggle_instalock(self):
        """
        Alterna o estado do Instalock entre habilitado e desabilitado.
        """
        self.instalock_enabled = not self.instalock_enabled
        status = "ON" if self.instalock_enabled else "OFF"

    def toggle_auto_ban(self):
        """
        Alterna o estado do AutoBan entre habilitado e desabilitado.
        """
        self.auto_ban_enabled = not self.auto_ban_enabled
        status = "ON" if self.auto_ban_enabled else "OFF"

    def start_threads(self):
        """
        Inicia as threads para rodar o Instalock e AutoBan.
        """
        threading.Thread(target=self.run_instalock, daemon=True).start()
        threading.Thread(target=self.run_auto_ban, daemon=True).start()