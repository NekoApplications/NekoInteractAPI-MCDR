import socket
import time

from mcdreforged.api.decorator import new_thread

socket_service_start = False


def set_socket_service_start(value: bool):
    global socket_service_start
    socket_service_start = value


class SocketService:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # @new_thread("NekoInteractAPI Socket Thread")
    def connect(self, host, port):
        # 绑定IP
        server_address = (host, port)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        # 连接
        self.sock.connect(server_address)
        
    def send_packet(self, packet_data: str):
        self.sock.send(packet_data.encode('utf-8'))
        
    def receive_packet(self) -> str:
        return self.sock.recv(1024).decode('utf-8')
    
    def close_connect(self):
        self.sock.close()
        
    @new_thread("NekoInteractAPI Socket Heartbeat")
    def send_heartbeat(self):
        while socket_service_start:
            self.sock.sendall(b"Heartbeat\n")
            time.sleep(30)
        