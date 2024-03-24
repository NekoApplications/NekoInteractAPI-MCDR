import json
import time
import websocket

from mcdreforged.api.decorator import new_thread

from .logger import logger
from .mcdr_utils import mcdr_utils

class WebSocketService:
    ws: websocket.WebSocketApp = None

    def __init__(self):
        self.available = False
    
    @new_thread("NekoInteractAPI Websocket Thread")
    def connect(self, host, port) -> None:
        self.ws = websocket.WebSocketApp(f"ws://{host}:{port}/",
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error)
        self.ws.run_forever(ping_interval=30, ping_timeout=5, ping_payload=f"Heartbeat_PING_{time.time()}")
        self.available = True
    
    def send(self, data: str):
        self.ws.send(data)
    
    def close(self) -> None:
        if self.ws:
            self.ws.close()
        self.ws = None
    
    def on_message(self, ws, message):
        self.message_handler(message)
    
    def on_error(self, ws, error):
        if self.available:
            logger.error("webSocket似乎发生了一个错误: " + str(error))
    
    def on_open(self, ws):
        ws.send(f"Connect_PACKET_{time.time()}")
    
    def message_handler(self, message: str) -> None:
        data = json.loads(message)
        try:
            response = globals()[data["service"].lower()](data)
        except KeyError:
            response = {
                "status": -1001,
                "service": data["service"],
                "requestId": data["requestId"],
                "message": "Service NotFound",
                "data": {}
            }
        self.send(json.dumps(response))
        
def mcdr_complete_command(data):
    suggestions = mcdr_utils.get_suggestions(data.get("data").get("command"))
    return {
        "status": 0,
        "service": data["service"],
        "requestId": data["requestId"],
        "message": "",
        "data": {
            "suggestions": json.dumps(suggestions)
        }
    }

def mcdr_send_command(data):
    return {
        "status": 0,
        "service": data["service"],
        "requestId": data["requestId"],
        "message": "",
        "data": {
            "response": mcdr_utils.send_command(data.get("data").get("command"))
        }
    }

def mcdr_permission_get(data):
    return {
        "status": 0,
        "service": data["service"],
        "requestId": data["requestId"],
        "message": "",
        "data": {
            "player": data["data"]["player"],
            "permission": str(mcdr_utils.get_player_permission(data.get("data").get("player")))
        }
    }

def mcdr_permission_list(data):
    perms = mcdr_utils.get_mcdr_permission()
    return {
        "status": 0,
        "service": data["service"],
        "requestId": data["requestId"],
        "message": "",
        "data": {
            "response": json.dumps(perms)
        }
    }

def mcdr_permission_set(data):
    result, msg = mcdr_utils.set_player_permission(data.get("data").get("player"), data.get("data").get("permission"))
    if result:
        return {
            "status": 0,
            "service": data["service"],
            "requestId": data["requestId"],
            "message": msg,
            "data": {
                "response": "success"
            }
        }
    else:
        return {
            "status": -1011,
            "service": data["service"],
            "requestId": data["requestId"],
            "message": msg,
            "data": {}
        }
