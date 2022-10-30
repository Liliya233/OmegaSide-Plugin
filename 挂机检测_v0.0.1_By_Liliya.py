# 插件: 开
from omega_side.python3_omega_sync import API
from omega_side.python3_omega_sync import frame as omega
from omega_side.python3_omega_sync.protocol import *
from API_By_Liliya import api
import json

class player(object):
    def __init__(self, UUID='', yRot='', time=0):
        # UUID
        self.UUID = UUID
        # 上次视角
        self.yRot = yRot
        # 挂机时间
        self.time = time

class plugin(object):
    def detect(self):
        # 新字典
        newDict = dict()
        # 发送指令
        response = self.api.do_send_ws_cmd("querytarget @a[tag=!omg]")
        # 没有目标则不处理
        if response.result.OutputMessages[0].Success:
            for data in json.loads(response.result.OutputMessages[0].Parameters[0]):
                playerObj = player(UUID=data['uniqueId'], yRot=data['yRot'])
                # 即使不动也会有细微偏差，所以取2位小数; 以及会出现某种奇妙的情况; **网易
                if playerObj.UUID in self.dict.keys():
                    if round(playerObj.yRot, 2) == round(self.dict[playerObj.UUID].yRot, 2) or 359 < abs(playerObj.yRot)+abs(self.dict[playerObj.UUID].yRot) < 361:
                        playerObj.time = self.dict[playerObj.UUID].time + 1
                    if playerObj.time > 30:
                        self.api.do_send_wo_cmd(f"kick \"{self.api.get_player_name(playerObj.UUID)}\" §c不允许长时间挂机")
                        continue
                newDict.update({data['uniqueId']: playerObj})
        # 替换为新字典以清除无用数据
        self.dict = newDict.copy()
        return

    def __call__(self, API:API):
        # 获取API
        self.api=api(API)
        # 数据记录
        self.dict=dict()
        # 注册功能
        self.api.execute_with_repeat(func=self.detect, repeat_time=60)

omega.add_plugin(plugin=plugin())
omega.run(addr=None)
