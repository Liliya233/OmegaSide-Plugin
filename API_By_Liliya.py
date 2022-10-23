import threading
import json
from omega_side.python3_omega_sync import API
from omega_side.python3_omega_sync.protocol import *

class api(object):
    def __init__(self, API:API) -> None:
        self.api = API
        self.json_lock = threading.Lock()

    def execute_after(self, func, *args, delay_time):
        return self.api.execute_after(func, *args, delay_time=delay_time)

    def execute_with_repeat(self, func, *args, repeat_time):
        return self.api.execute_with_repeat(func, *args, repeat_time=repeat_time)

    def execute_in_individual_thread(self, func, *args):
        return self.api.execute_in_individual_thread(func, *args)

    def do_echo(self, msg, cb=None):
        return self.api.do_echo(msg=msg, cb=cb)

    def do_send_ws_cmd(self, cmd, cb=None):
        return self.api.do_send_ws_cmd(cmd=cmd, cb=cb)

    def do_send_player_cmd(self, cmd, cb=None):
        return self.api.do_send_player_cmd(cmd=cmd, cb=cb)

    def do_send_wo_cmd(self, cmd, cb=None):
        return self.api.do_send_wo_cmd(cmd=cmd, cb=cb)

    def do_get_uqholder(self, cb=None):
        return self.api.do_get_uqholder(cb=cb)

    def do_get_players_list(self, cb=None):
        return self.api.do_get_players_list(cb=cb)

    def do_get_get_player_next_param_input(self, player, hint="", cb=None):
        return self.api.do_get_get_player_next_param_input(player=player, hint=hint, cb=cb)

    def do_send_player_msg(self, player, msg, cb=None):
        return self.api.do_send_player_msg(player=player, msg=msg, cb=cb)

    def do_set_player_title(self, player, msg, cb=None):
        return self.api.do_set_player_title(player=player, msg=msg, cb=cb)

    def do_set_player_subtitle(self, player, msg, cb=None):
        return self.api.do_set_player_subtitle(player=player, msg=msg, cb=cb)

    def do_set_player_actionbar(self, player, msg, cb=None):
        return self.api.do_set_player_actionbar(player=player, msg=msg, cb=cb)

    def do_get_player_pos(self, player, limit, cb=None):
        return self.api.do_get_player_pos(player=player, limit=limit, cb=cb)

    def do_set_player_data(self, player, entry, data, cb=None):
        return self.api.do_set_player_data(player=player, entry=entry, data=data, cb=cb)

    def do_get_player_data(self, player, entry, cb=None):
        return self.api.do_get_player_data(player=player, entry=entry, cb=cb)

    def do_get_item_mapping(self, cb=None):
        return self.api.do_get_item_mapping(cb=cb)

    def do_get_block_mapping(self, cb=None):
        return self.api.do_get_block_mapping(cb=cb)

    def do_get_scoreboard(self, cb=None):
        return self.api.do_get_scoreboard(cb=cb)

    def do_send_fb_cmd(self, cmd, cb=None):
        return self.api.do_send_fb_cmd(cmd=cmd, cb=cb)

    def do_send_qq_msg(self, msg, cb=None):
        return self.api.do_send_qq_msg(msg=msg, cb=cb)

    def listen_omega_menu(self, triggers=[], argument_hint="", usage="", on_menu_invoked=None, cb=None):
        return self.api.listen_omega_menu(triggers=triggers, argument_hint=argument_hint, usage=usage, on_menu_invoked=on_menu_invoked, cb=cb)

    def listen_mc_packet(self, pkt_type, on_new_packet_cb, cb=None):
        return self.api.listen_mc_packet(pkt_type=pkt_type, cb=cb, on_new_packet_cb=on_new_packet_cb)

    def listen_any_mc_packet(self, on_new_packet_cb, cb=None):
        return self.api.listen_any_mc_packet(cb=cb, on_new_packet_cb=on_new_packet_cb)

    def listen_player_login(self, on_player_login_cb, cb=None):
        return self.api.listen_player_login(cb=cb, on_player_login_cb=on_player_login_cb)

    def listen_player_logout(self, on_player_logout_cb, cb=None):
        return self.api.listen_player_logout(cb=cb, on_player_logout_cb=on_player_logout_cb)

    def listen_block_update(self, on_block_update, cb=None):
        return self.api.listen_block_update(cb=cb, on_block_update=on_block_update)

    # 写入数据到JSON文件
    def write_json_file(self, filename, dict):
        try:
            self.json_lock.acquire()
            with open(f"./data/{filename}.json", 'w', encoding='utf-8') as file:
                json.dump(dict, file, indent=4, ensure_ascii=False)
        except Exception:
            return False
        finally:
            self.json_lock.release()
        return True

    # 从JSON文件读取数据
    def read_json_file(self, filename):
        try:
            self.json_lock.acquire()
            with open(f"./data/{filename}.json", 'r', encoding='utf-8') as file:
                result = json.load(file)
        except Exception:
            result = {}
        finally:
            self.json_lock.release()
        return result

    # 为玩家存储一个数据
    def set_player_data(self, player, key, value):
        # 获取UUID
        UUID = self.get_player_uuid(player)
        # 获取JSON数据
        dict = self.read_json_file("playerData_By_Liliya")
        # 写入JSON数据
        if dict is not False:
            # 如果不存在该UUID，则创建
            if UUID not in dict.keys():
                dict.update({UUID: {}})
            # 写入数据
            dict[UUID].update({key: value})
            self.write_json_file("playerData_By_Liliya", dict)
            return True
        return False

    # 为玩家删除一个数据
    def del_player_data(self, player, key):
        # 获取UUID
        UUID = self.get_player_uuid(player)
        # 获取JSON数据
        dict = self.read_json_file("playerData_By_Liliya")
        # 删除JSON数据
        try:
            dict[UUID].pop(key)
            self.write_json_file("playerData_By_Liliya", dict)
        except Exception:
            return False
        return True

    # 读取一个玩家数据
    def get_player_data(self, player, key):
        # 获取UUID
        UUID = self.get_player_uuid(player)
        # 获取JSON数据
        dict = self.read_json_file("playerData_By_Liliya")
        # 解析
        try:
            return dict[UUID][key]
        except Exception:
            return None

    # 通过玩家UUID查询名字
    def get_player_name(self, UUID):
        for player in self.do_get_players_list():
            if(player.uuid == UUID):
                return player.name
        return None

    # 通过玩家名查询UUID
    def get_player_uuid(self, name):
        for player in self.do_get_players_list():
            if(player.name == name):
                return player.uuid
        return None

    # 根据玩家名查询权限等级
    def get_player_permission(self, name):
        # 获取uqholder
        uqholder = self.do_get_uqholder()
        # 权限列表
        OPPermissionLevelList = ["访客", "成员", "操作员"]
        # 解析
        for data in uqholder.PlayersByEntityID.values():
            if data.Username == name:
                try:
                    return OPPermissionLevelList[data.OPPermissionLevel]
                except Exception:
                    return f'unknow<{data.OPPermissionLevel}>'
        return None

    # 根据玩家名查询操作系统
    def get_player_platform(self, name):
        # 获取uqholder
        uqholder = self.do_get_uqholder()
        # 平台ID列表 - From PhoenixBuilder:minecraft/protocol/os.go
        platformIDList = ["Android", "iOS", "OSX", "FireOS", "GearVR", "Hololens", "Win10", "Win32", "Dedicated", "TVOS", "Orbis", "NX", "XBOX", "WP"]
        # 解析
        for data in uqholder.PlayersByEntityID.values():
            if data.Username == name:
                try:
                    return platformIDList[data.BuildPlatform - 1]
                except Exception:
                    return f'unknow<{data.BuildPlatform}>'
        return None

    # 根据玩家名查询设备ID (需要前置插件:设备记录)
    def get_player_device_id(self, name):
        return self.get_player_data(name, "DeviceID")

    # 根据玩家名查询皮肤ID
    def get_player_skin_id(self, name):
        # 获取uqholder
        uqholder = self.do_get_uqholder()
        # 解析
        for data in uqholder.PlayersByEntityID.values():
            if data.Username == name:
                return data.SkinID
        return None

    # 根据玩家名查询维度与位置信息
    def get_player_pos(self, name):
        # 发送指令
        response = self.do_send_ws_cmd(f"querytarget @a[name=\"{name}\"]")
        try:
        # 解析
            for data in json.loads(response.result.OutputMessages[0].Parameters[0]):
                result = {}
                result.update({"d": data['dimension']})
                result.update({"x": int(data['position']['x'])})
                result.update({"y": int(data['position']['y'])})
                result.update({"z": int(data['position']['z'])})
                return result
        except Exception:
            return None

    # 获取玩家分数
    def get_player_score(self, name, scoreboard):
        # 发送指令
        response = self.do_send_ws_cmd(f"scoreboard players add @a[name=\"{name}\"] {scoreboard} 0")
        # 解析
        if response.result.OutputMessages[0].Success:
            return response.result.OutputMessages[0].Parameters[3]
        return None

    # 设置玩家分数
    def set_player_score(self, name, scoreboard, score):
        response = self.do_send_ws_cmd(f"scoreboard players set @a[name=\"{name}\"] {scoreboard} {score}")
        # 解析
        if response.result.OutputMessages[0].Success:
            return True
        return False

    # 增加玩家分数
    def add_player_score(self, name, scoreboard, score):
        response = self.do_send_ws_cmd(f"scoreboard players add @a[name=\"{name}\"] {scoreboard} {score}")
        # 解析
        if response.result.OutputMessages[0].Success:
            return True
        return False

    # 扣除玩家分数 - 扣除后小于0则失败
    def remove_player_score(self, name, scoreboard, score):
        response = self.do_send_ws_cmd(f"scoreboard players remove @a[name=\"{name}\",scores={{{scoreboard}={score}..}}] {scoreboard} {score}")
        # 解析
        if response.result.OutputMessages[0].Success:
            return True
        return False

    # 向所有玩家发送一条消息
    def send_all_player_msg(self, msg):
        self.execute_after(func=lambda:self.do_send_wo_cmd(f"tellraw @a {{\"rawtext\":[{{\"text\":\"{msg}\"}}]}}"), delay_time=0.1)
        return True
