import threading
import time
from Rengar import Rengar  # Importando a classe Rengar para realizar as requisições
from champion_converter import ChampionConverter  # Importa a classe ChampionConverter
import random

class InstalockAutoban:
    def __init__(self):
        self.instalock_enabled = False
        self.instalock_champion = "Random"
        self.auto_ban_enabled = False
        self.auto_ban_champion = "None"
        self.rengar = Rengar()  # Instância da classe Rengar para fazer requisições
        self.champion_converter = ChampionConverter(self.rengar)  # Instância da classe ChampionConverter
        self.champion_converter.update_champion_list()  # Atualiza a lista de campeões ao iniciar

    def set_instalock_champion(self, champion_name):
        if champion_name == "99":
            self.instalock_enabled = False
            self.instalock_champion = "None"
            # print("Instalock has been disabled.")
        else:
            champ_id = self.champion_converter.champ_name_to_id(champion_name)
            if champ_id == -1:
                print(f"Champion '{champion_name}' not found.")
            else:
                self.instalock_champion = champion_name
                self.instalock_enabled = True
                # print(f"Instalock champion set to: {champion_name} (ID: {champ_id})")
                # print("Instalock is now ON.")

    def set_auto_ban_champion(self, champion_name):
        if champion_name == "99":
            self.auto_ban_enabled = False
            self.auto_ban_champion = "None"
            # print("AutoBan has been disabled.")
        else:
            champ_id = self.champion_converter.champ_name_to_id(champion_name)
            if champ_id == -1:
                print(f"Champion '{champion_name}' not found.")
            else:
                self.auto_ban_champion = champion_name
                self.auto_ban_enabled = True
                # print(f"AutoBan champion set to: {champion_name} (ID: {champ_id})")
                # print("AutoBan is now ON.")

    def monitor_champ_select(self):
        """
        Monitora continuamente o estado da seleção de campeões e executa
        Instalock ou AutoBan quando apropriado.
        """
        while True:
            # print("Checking for Champion Select...")
            try:
                champ_select_resp = self.rengar.lcu_request("GET", "/lol-champ-select/v1/session", "")
                if "RPC_ERROR" not in champ_select_resp.text:

                    root_champ_select = champ_select_resp.json()
                    cell_id = root_champ_select.get("localPlayerCellId")

                    if cell_id == None:
                        #print("Local player ID not found.")
                        time.sleep(0.3)
                        continue

                    for actions in root_champ_select["actions"]:
                        if not isinstance(actions, list):
                            continue
                        for action in actions:
                            if self.instalock_enabled and action["actorCellId"] == cell_id and action["type"] == "pick" and not action["completed"]:
                                
                                time.sleep(0.3)  # Simulando um pequeno delay

                                if self.instalock_champion == "Random":
                                    instalock_champs = self.champion_converter.get_instalock_champs()
                                    champion_id = random.choice(instalock_champs)[0]
                                else:
                                    champion_id = self.champion_converter.champ_name_to_id(self.instalock_champion)

                                # print(f"Picking champion {self.instalock_champion} (ID: {champion_id})")

                                patch_resp = self.rengar.lcu_request(
                                    "PATCH",
                                    f"/lol-champ-select/v1/session/actions/{action['id']}",
                                    {"completed": True, "championId": champion_id}
                                )

                                # if patch_resp.status_code == 204:  # 204 = sucesso sem conteúdo
                                #     print(f"Champion {self.instalock_champion} selected successfully.")
                                # else:
                                #     print(f"Failed to select champion. Status code: {patch_resp.status_code}")
                                # continue  # Após o pick, interrompe o loop para evitar múltiplos picks

                                time.sleep(0.3)  # Verifica o estado novamente após uma pausa


                            elif self.auto_ban_enabled and action["actorCellId"] == cell_id and action["type"] == "ban" and not action["completed"]:
                                time.sleep(0.3)  # Simulando um pequeno delay
                                champion_id = self.champion_converter.champ_name_to_id(self.auto_ban_champion)

                                #print(f"Banning champion {self.auto_ban_champion} (ID: {champion_id})")

                                patch_resp = self.rengar.lcu_request(
                                    "PATCH",
                                    f"/lol-champ-select/v1/session/actions/{action['id']}",
                                    {"completed": True, "championId": champion_id}
                                )

                                # if patch_resp.status_code == 204:
                                #     print(f"Champion {self.auto_ban_champion} banned successfully.")
                                # else:
                                #     pass
                                #      print(f"Failed to ban champion. Status code: {patch_resp.status_code}")
                                continue


                                time.sleep(0.3)  # Verifica o estado novamente após uma pausa


                    # print("Champion Select found, running Instalock and AutoBan if enabled...")
                else:
                    pass
                    # print("Not in Champion Select phase.")
                time.sleep(0.3)  # Verifica a cada 5 segundos
            except:
                pass

    def toggle_instalock(self):
        """
        Alterna o estado do Instalock entre habilitado e desabilitado.
        """
        self.instalock_enabled = not self.instalock_enabled
        status = "ON" if self.instalock_enabled else "OFF"
        # print(f"Instalock is now {status}")

    def toggle_auto_ban(self):
        """
        Alterna o estado do AutoBan entre habilitado e desabilitado.
        """
        self.auto_ban_enabled = not self.auto_ban_enabled
        status = "ON" if self.auto_ban_enabled else "OFF"
        # print(f"AutoBan is now {status}")

    def start_threads(self):
        """
        Inicia as threads para rodar o Instalock e AutoBan.
        """
        threading.Thread(target=self.run_instalock, daemon=True).start()
        threading.Thread(target=self.run_auto_ban, daemon=True).start()

