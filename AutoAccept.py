import threading
import time
from Rengar import Rengar

class autoaccept:
    def __init__(self):
        self.auto_accept_enabled = False
        self.rengar = Rengar()

    def toggle_auto_accept(self):
        self.auto_accept_enabled = not self.auto_accept_enabled
        state = "ON" if self.auto_accept_enabled else "OFF"
        print(f"Auto accept is now {state}.")

    def accept_match(self, match_id):
        # Endpoint para aceitar partida
        response = self.rengar.lcu_request("POST", f"/lol-matchmaking/v1/ready-check/accept", "")
        #if response.status_code == 200:
        #    print(f"\nAccepted match\n")
        #else:
        #    print(f"Failed to accept match with ID: {match_id}. Status code: {response.status_code}")

    def auto_accept_matches(self):
        while True:
            if self.auto_accept_enabled:
                # Faz a requisição para verificar o estado da busca por partida
                response = self.rengar.lcu_request("GET", "/lol-lobby/v2/lobby/matchmaking/search-state", "")
                
                if response.status_code == 200:
                    match_data = response.json()
                    
                    # Exibe o conteúdo da resposta para verificar o estado do matchmaking
                    #print("Matchmaking Data:", match_data)

                    # Verifica se o status indica que o jogador está em um ready-check
                    if match_data.get("searchState") == "Found":
                    #    print("Match found, ready to accept.")
                        self.accept_match(None)  # Não há um ID de partida, basta aceitar
                    #else:
                    #    print(f"Current search state: {match_data.get('searchState')}")
                elif response.status_code == 404:
                    # Estado 404 é esperado quando não há uma busca ativa, então evitamos o spam de erro
                    print("No active matchmaking search.")
                else:
                    print(f"Failed to fetch matchmaking state. Status code: {response.status_code}")
            
            time.sleep(1)  # Checa a cada 5 segundos


