# 插件: 开
from omega_side.python3_omega_sync import API
from omega_side.python3_omega_sync import frame as omega
from omega_side.python3_omega_sync.protocol import *
from API_By_Liliya import api

class infoPlugin(object):
    def on_call(self, input:PlayerInput):
        # 获取昵称
        player = input.Name
        # 输出个人信息头部
        self.api.do_send_player_msg(player, "§l§aINFORMATION - 个人信息")
        # 输出玩家信息
        self.api.do_send_player_msg(player, f"§l■§e昵称： §r{player}")
        self.api.do_send_player_msg(player, f"§l■§eID： §r{self.api.get_player_score(player, 'ID')}")
        self.api.do_send_player_msg(player, f"§l■§eUUID： §r{self.api.get_player_uuid(player)}")
        self.api.do_send_player_msg(player, f"§l■§e权限： §r{self.api.get_player_permission(player)}")
        self.api.do_send_player_msg(player, f"§l■§e系统： §r{self.api.get_player_platform(player)}")
        self.api.do_send_player_msg(player, f"§l■§e设备ID： §r{self.api.get_player_device_id(player)}")
        self.api.do_send_player_msg(player, f"§l■§e皮肤ID： §r{self.api.get_player_skin_id(player)}")
        # 输出资产信息头部
        self.api.do_send_player_msg(player, "§l§aINFORMATION - 资产信息")
        # 输出资产信息
        self.api.do_send_player_msg(player, f"§l■§e在线： §r{self.api.get_player_score(player, 'online')}")
        self.api.do_send_player_msg(player, f"§l■§e家园ID： §r{self.api.get_player_score(player, '家园_主人ID')}")
        self.api.do_send_player_msg(player, f"§l■§e结晶碎片： §r{self.api.get_player_score(player, 'money')}")
        # 输出尾部
        self.api.do_send_player_msg(player, "§l§aINFORMATION - 显示完毕")
        return

    def __call__(self, API:API):
        # 获取API
        self.api=api(API)
        # 注册菜单
        self.api.listen_omega_menu(triggers=["info"], argument_hint="", usage="查询个人信息", on_menu_invoked=self.on_call)

omega.add_plugin(plugin=infoPlugin())
omega.run(addr=None)
