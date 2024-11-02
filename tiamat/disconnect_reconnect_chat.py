from Rengar import Rengar

rengar = Rengar()


class Chat:
    def __init__(self):
        self.chat_state = False

    def disconnect(self):
        body = {"config": "disable"}
        response = rengar.riot_request("POST", "/chat/v1/suspend", body)
        print(response.text)  # Troquei `input` por `print` para exibir a resposta

    def reconnect(self):
        response = rengar.riot_request("POST", "/chat/v1/resume", "")

    def toggle_chat(self):
        self.chat_state = not self.chat_state
        if self.chat_state:
            self.disconnect()
        else:
            self.reconnect()

    def return_state(self):
        if not self.chat_state:
            return "ON"
        else:
            return "OFF"
