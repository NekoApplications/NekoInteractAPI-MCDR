import re
import json

from typing import Callable
from mcdreforged.command.command_source import CommandSource
from mcdreforged.info_reactor.info import Info
from mcdreforged.mcdr_server import MCDReforgedServer
from mcdreforged.plugin.plugin_registry import PluginCommandHolder
from mcdreforged.plugin.server_interface import PluginServerInterface

from .command_exporter import Node
from .websocket_service import WebSocketService
from .config import Configuration
from .constant import CONFIG_FILE

websocket_service = WebSocketService()

server_inst: PluginServerInterface
config: Configuration
mcdr_server: MCDReforgedServer
old_on_plugin_registry_changed: Callable


def get_node_json():
    root_nodes = mcdr_server.command_manager.root_nodes
    json_data = {'data': []}
    for key, value in root_nodes.items():
        plugin_command_holder: PluginCommandHolder = value[0]
        json_data['data'].append(Node(key, plugin_command_holder.node).dict)
    websocket_service.ws.send(json.dumps(json_data))

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
    global server_inst, mcdr_server
    server_inst = server
    mcdr_server = server._mcdr_server
    
    load_config()
    
    # getNode
    if config.enable:
        get_node_json()
    global old_on_plugin_registry_changed
    old_on_plugin_registry_changed = mcdr_server.on_plugin_registry_changed
    
    def new_on_plugin_registry_changed():
        server.logger.debug('on_plugin_registry_changed')
        old_on_plugin_registry_changed()
        if config.enable:
            get_node_json()
    
    mcdr_server.on_plugin_registry_changed = new_on_plugin_registry_changed


def on_unload(server: PluginServerInterface):
    websocket_service.close()
    mcdr_server.on_plugin_registry_changed = old_on_plugin_registry_changed
