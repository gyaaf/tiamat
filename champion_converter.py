import requests

class ChampionConverter:
    def __init__(self, rengar):
        self.rengar = rengar  # Instância da classe Rengar
        self.champ_dict = {}  # Dicionário para armazenar nome e ID dos campeões

    def update_champion_list(self):
        """
        Atualiza a lista de campeões obtendo seus IDs e nomes da API LCU.
        """
        print("Fetching champion list from LCU...")
        response = self.rengar.lcu_request("GET", "/lol-champ-select/v1/all-grid-champions", "")
        
        if response.status_code == 200:
            champion_data = response.json()
            for champ in champion_data:
                champ_id = champ["id"]
                champ_name = champ["name"]
                self.champ_dict[champ_name.lower()] = champ_id  # Armazena o nome em minúsculas para fácil busca
            print("Champion list updated successfully.")
        else:
            print("Failed to fetch champion data.")

    def champ_name_to_id(self, champ_name):
        """
        Converte o nome de um campeão para o ID correspondente.
        Se o campeão não for encontrado, retorna -1.
        """
        champ_name = champ_name.lower()  # Normaliza o nome do campeão para minúsculas
        return self.champ_dict.get(champ_name, -1)  # Retorna o ID do campeão ou -1 se não encontrado
