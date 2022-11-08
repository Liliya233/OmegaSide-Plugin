# 插件: 开
# Name：睡觉检测
# Version：0.0.1
# Author：Liliya233
from omega_side.python3_omega_sync import API
from omega_side.python3_omega_sync import frame as omega
from omega_side.python3_omega_sync.protocol import *
from API_By_Liliya import api
import time

class sleepDetect:
    # 初始化
    def __init__(self):
        self.sleepPercentage = 0.5

    # 判断是否满足跳过条件
    def isSatisfy(self, eventData):
        # Mojang ??
        plTotal , plsleeping= int(eventData) // 65536, int(eventData) % 65536
        # 人数变动时也会触发此事件，加个辨别吧
        # PS：如果不处于夜晚或者雷雨天
        if not (12000 <= int(self.api.do_send_ws_cmd("time query daytime").result.OutputMessages[0].Parameters[0]) <= 24000
            or self.api.do_send_ws_cmd("weather query").result.OutputMessages[0].Parameters[0] == "%commands.weather.query.thunder"):
            return
        # 判断睡觉的玩家是否满足设定的比例值
        if plsleeping/plTotal >= self.sleepPercentage:
            self.api.send_all_player_msg("§b半数玩家已睡眠，将跳过黑夜或雷雨天")
            time.sleep(5)
            self.api.do_send_wo_cmd("time set 0")
            self.api.do_send_wo_cmd("weather clear")
        else:
            self.api.send_all_player_msg(f"§b要想跳过黑夜或雷雨天，还需§e {int(plTotal/2)+1-plsleeping} §b名玩家进入睡眠")
        
    # 接收到特定事件数据包时进行处理
    def dealIDLevelEvent(self, packet):
        if packet.EventType == 9801:
            self.api.execute_in_individual_thread(self.isSatisfy, packet.EventData)

    def __call__(self, API:API):
        # 获取API
        self.api=api(API)
        # 注册监听
        self.api.listen_mc_packet(pkt_type="IDLevelEvent", on_new_packet_cb=self.dealIDLevelEvent)

omega.add_plugin(plugin=sleepDetect())
omega.run(addr=None)
