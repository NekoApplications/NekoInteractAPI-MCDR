from mcdreforged.utils.serializer import Serializable


class Configuration(Serializable):
    enable: bool = True
    websocket_host: str = 'localhost'
