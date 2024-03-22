from mcdreforged.utils.serializer import Serializable


class Configuration(Serializable):
    enable: bool = True
    socket_host: str = 'localhost'
    node_path: str = 'server/config/node.json'
