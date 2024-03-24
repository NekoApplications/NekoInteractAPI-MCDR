from typing import Union

from mcdreforged.command.command_source import PluginCommandSource
from mcdreforged.minecraft.rtext.text import RTextBase
from mcdreforged.permission.permission_level import PermissionLevel
from mcdreforged.plugin.server_interface import PluginServerInterface, ServerInterface
from mcdreforged.utils.types import MessageText


class ControllerCommandSource(PluginCommandSource):
    def __init__(self, server: ServerInterface):
        super().__init__(server)
        self.messages = []
        self.server = server
    
    def get_server(self) -> 'ServerInterface':
        return self.server
    
    @property
    def is_player(self) -> bool:
        return False
    
    @property
    def is_console(self) -> bool:
        return True
    
    def get_permission_level(self) -> int:
        return 2147483647
    
    def reply(self, message: MessageText, **kwargs) -> None:
        if isinstance(message, str):
            self.messages.append(message.format(**kwargs))
        elif isinstance(message, RTextBase):
            self.messages.append(message.to_plain_text())


class MCDRUtils:
    server: PluginServerInterface
    
    def set_server(self, server: PluginServerInterface):
        self.server = server
    
    def get_suggestions(self, incomplete_command) -> list[str]:
        command_manager = self.server._mcdr_server.command_manager
        suggestions = []
        for s in command_manager.suggest_command(incomplete_command, self.server.get_plugin_command_source()):
            if s.suggest_input != incomplete_command:
                suggestions.append(s.suggest_input)
        return suggestions
    
    def send_command(self, complete_command) -> str:
        command_source = ControllerCommandSource(self.server)
        self.server.execute_command(complete_command, command_source)
        return "\n".join(command_source.messages)
    
    def get_player_permission(self, player: str) -> int:
        result = self.server.get_permission_level(player)
        if not result:
            return PermissionLevel.from_value(self.server._mcdr_server.permission_manager.get_default_permission_level()).level
        else:
            return result
    
    def get_mcdr_permission(self) -> dict[str, list[str]]:
        permission_manager = self.server._mcdr_server.permission_manager
        result = {}
        for p in PermissionLevel.LEVELS:
            result[PermissionLevel.from_value(p).name] = permission_manager.get_permission_group_list(p)
        return result
    
    def set_player_permission(self, player: str, value: Union[int, str]) -> tuple[bool, str]:
        try:
            self.server.set_permission_level(player, value)
            self.server.reload_permission_file()
            return True, ""
        except TypeError:
            return False, "Level NotFound"


mcdr_utils = MCDRUtils()
