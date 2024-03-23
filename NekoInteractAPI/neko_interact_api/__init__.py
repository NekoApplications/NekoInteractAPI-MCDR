import re

from mcdreforged.command.command_source import CommandSource
from mcdreforged.info_reactor.info import Info
from mcdreforged.plugin.server_interface import PluginServerInterface

from .websocket_service import WebSocketService
from .config import Configuration
from .constant import CONFIG_FILE
from . mcdr_utils import mcdr_utils

websocket_service = WebSocketService()

server_inst: PluginServerInterface
config: Configuration

def on_info(server: PluginServerInterface, info: Info):
    if not info.is_user and info.content.startswith("[NekoInteractAPI]"):
        match = re.match(r"\[NekoInteractAPI] Socket Port: (6553[0-5]|655[0-2]\d|65[0-4]\d{2}|6[0-4]\d{3}|[1-5]\d{4}|\d{1,4})", info.content)
        port = match.group(1)
        if config.enable:
            websocket_service.connect(config.websocket_host, port)


def load_config(source: CommandSource or None = None):
    global config
    config = server_inst.load_config_simple(CONFIG_FILE, target_class=Configuration, in_data_folder=False, source_to_reply=source)


def on_load(server: PluginServerInterface, old):
    global server_inst
    server_inst = server
    
    mcdr_utils.set_server(server)
    
    load_config()

def on_unload(server: PluginServerInterface):
    websocket_service.close()
