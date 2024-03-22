import json
import os
import re
from pathlib import Path
from typing import Callable

from mcdreforged.command.command_source import CommandSource
from mcdreforged.info_reactor.info import Info
from mcdreforged.mcdr_server import MCDReforgedServer
from mcdreforged.plugin.plugin_registry import PluginCommandHolder
from mcdreforged.plugin.server_interface import PluginServerInterface

from NekoInteractAPI.neko_interact_api.command_exporter import Node
from socket_service import SocketService, set_socket_service_start
from config import Configuration
from constant import CONFIG_FILE

socket_service = SocketService()

server_inst: PluginServerInterface
config: Configuration
mcdr_server: MCDReforgedServer
old_on_plugin_registry_changed: Callable


def get_node_json(path: str):
    path = Path(path)
    if not os.path.exists(path.parent):
        os.makedirs(path.parent)
    root_nodes = mcdr_server.command_manager.root_nodes
    json_data = {'data': []}
    for key, value in root_nodes.items():
        plugin_command_holder: PluginCommandHolder = value[0]
        json_data['data'].append(Node(key, plugin_command_holder.node).dict)
    print(path)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4)


def on_info(server: PluginServerInterface, info: Info):
    if not info.is_user and info.content.startswith("[NekoInteractAPI]"):
        match = re.match(r"\[NekoInteractAPI] Socket Port: (6553[0-5]|655[0-2]\d|65[0-4]\d{2}|6[0-4]\d{3}|[1-5]\d{4}|\d{1,4})", info.content)
        port = match.group(1)
        if config.enable:
            socket_service.connect(config.socket_host, port)


def load_config(source: CommandSource or None = None):
    global config
    config = server_inst.load_config_simple(CONFIG_FILE, target_class=Configuration, in_data_folder=False, source_to_reply=source)


def on_load(server: PluginServerInterface, old):
    global server_inst, mcdr_server
    server_inst = server
    mcdr_server = server._mcdr_server
    
    # Socket
    load_config()
    set_socket_service_start(True)
    
    # getNode
    get_node_json(config.node_path)
    global old_on_plugin_registry_changed
    old_on_plugin_registry_changed = mcdr_server.on_plugin_registry_changed
    
    def new_on_plugin_registry_changed():
        server.logger.debug('on_plugin_registry_changed')
        old_on_plugin_registry_changed()
        get_node_json(config.node_path)
    
    mcdr_server.on_plugin_registry_changed = new_on_plugin_registry_changed


def on_unload(server: PluginServerInterface):
    set_socket_service_start(False)
    socket_service.close_connect()
    mcdr_server.on_plugin_registry_changed = old_on_plugin_registry_changed
