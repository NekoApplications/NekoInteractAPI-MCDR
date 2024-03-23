import time
import websocket
from mcdreforged.api.decorator import new_thread

from .logger import logger

class WebSocketService:
    ws: websocket.WebSocketApp = None
    
    @new_thread("NekoInteractAPI Websocket Thread")
    def connect(self, host, port):
        self.ws = websocket.WebSocketApp(f"ws://{host}:{port}/",
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.run_forever(ping_interval=30, ping_timeout=5, ping_payload=f"Heartbeat_PING_{time.time()}")
    
    def send(self, data: str):
        self.ws.send(data)
    
    def close(self):
        if self.ws:
            self.ws.close()
        self.ws = None
    
    def on_message(self, ws, message):
        # Packet Handler
        ...
    
    def on_error(self, ws, error):
        logger.error("webSocket似乎发生了一个错误: " + error)
    
    def on_close(self, ws, close_status_code, close_msg):
        logger.info("webSocket连接已关闭, 关闭代码: " + close_status_code)
        self.ws = None
    
    def on_open(self, ws):
        ws.send(f"Connect_PACKET_{time.time()}")
