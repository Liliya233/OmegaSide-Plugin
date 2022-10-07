# 插件: 开
from omega_side.python3_omega_sync import API
from omega_side.python3_omega_sync import frame as omega
from omega_side.python3_omega_sync.protocol import *
from API_By_Liliya import api

class deviceRecord:
    def record(self, player, device):
        # 写入数据
        self.api.set_player_data(player, "DeviceID", device)
        return

    def on_add_player(self, packet):
        # 或许需要在新线程里执行
        self.api.execute_in_individual_thread(self.record, packet.Username, packet.DeviceID)
        return

    def __call__(self, API:API):
        # 获取API
        self.api=api(API)
        # 注册监听
        self.api.listen_mc_packet(pkt_type="IDAddPlayer", on_new_packet_cb=self.on_add_player)
        
omega.add_plugin(plugin=deviceRecord())
omega.run(addr=None)

