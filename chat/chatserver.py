from simple_websocket_server import WebSocketServer, WebSocket
import json

def get_msg_content(message):
    msg_content = json.loads(message)
    return msg_content  

def preparemessage(message_obj):
    msg_to_send = {"color":"black"}
    if message_obj['type'] == 'login':
        msg_to_send['content'] = f"{message_obj['username']} has been connected.\n"
        msg_to_send['color'] = "green"
    else:
        msg_to_send['content'] = f"{message_obj['username']}:{message_obj['body']}"

    msg_to_send = json.dumps(msg_to_send)
    return  msg_to_send

class ChatServer(WebSocket):
    clients = []

    @classmethod
    def send_to_all(cls, message):
        for client in cls.clients:
            client.send_message(message)

    def handle(self):  
        print(f"message received :{self.data},{type(self.data)}")  
        msg_content = get_msg_content(self.data) 
        self.username = msg_content['username']
        msg_to_send= preparemessage(msg_content)
        ChatServer.send_to_all(msg_to_send)


    def connected(self):  
        ChatServer.clients.append(self) 
        print(f"No of connected clients ={len(ChatServer.clients)}")

    def handle_close(self): 
        msg = {"content": f"{self.username} has been disconnected\n",
               "color":"red"}
        ChatServer.clients.remove(self)
        msg_to_send = json.dumps(msg)
        ChatServer.send_to_all(msg_to_send)







if __name__ == "__main__":
    print("--- server started")
    server = WebSocketServer('', 8800, ChatServer)
    server.serve_forever()
