# 插件: 开
# Name：设备记录
# Version：0.0.2
# Author：Liliya233
from omega_side.python3_omega_sync import API
from omega_side.python3_omega_sync import frame as omega
from omega_side.python3_omega_sync.protocol import *
from API_By_Liliya import api

class deviceRecord:
    # 写入数据
    def record(self, player, device):
        self.api.set_player_data(player, "DeviceID", device)
        return

    # 接收到玩家信息数据包时
    def on_add_player(self, packet):
        # 或许需要在新线程里执行
        self.api.execute_in_individual_thread(self.record, packet.Username, packet.DeviceID)
        return

    # 为了及时获取到数据，会在玩家完成登录后进行传送
    def on_login(self, packet):
        if packet.TextType == 2 and packet.Message == "§e%multiplayer.player.joined":
            self.api.execute_after(func=lambda:self.api.do_send_wo_cmd(f"execute @a[name=\"{packet.Parameters[0]}\"] ~~~ tp @a[tag=omg] ~ 320 ~"), delay_time=10)
        return

    def __call__(self, API:API):
        # 获取API
        self.api=api(API)
        # 注册监听
        self.api.listen_mc_packet(pkt_type="IDAddPlayer", on_new_packet_cb=self.on_add_player)
        self.api.listen_mc_packet(pkt_type="IDText", on_new_packet_cb=self.on_login)

omega.add_plugin(plugin=deviceRecord())
omega.run(addr=None)
