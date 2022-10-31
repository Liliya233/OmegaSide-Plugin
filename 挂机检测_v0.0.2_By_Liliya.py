# 插件: 开
from omega_side.python3_omega_sync import API
from omega_side.python3_omega_sync import frame as omega
from omega_side.python3_omega_sync.bootstrap import install_lib
from omega_side.python3_omega_sync.protocol import *
from API_By_Liliya import api
import json
import random

install_lib(lib_name="func_timeout",lib_install_name="func_timeout")
import func_timeout

class player(object):
    def __init__(self, UUID='', yRot='', posx='', posz='', time=1, expire=15):
        # UUID
        self.UUID = UUID
        # 上次视角
        self.yRot = yRot
        # 上次X轴坐标
        self.posx = posx
        # 上次Z轴坐标
        self.posz = posz
        # 挂机时间
        self.time = time
        # 保存时间 - 玩家退出登录后，记录应被保存一段时间
        self.expire = expire

class plugin(object):
    def __init__(self):
        # 数据记录
        self.dict_yRot=dict()
        self.dict_distance=dict()
        
    def kick(self, playerName):
        self.api.do_send_wo_cmd(f"kick \"{playerName}\" §c疑似长时间挂机，请重新登录")

    @func_timeout.func_set_timeout(30)
    def verify_in_time(self, playerName):
        chance = 3
        while True:
            x = random.randrange(1, 25)
            y = random.randrange(1, 25)
            input = self.api.do_get_get_player_next_param_input(playerName, f"§e[挂机检测] §c请在§e30秒内§c计算并发送 §e{x}+{y} §c进行验证，否则服务器将会断开连接！")
            if input.err == "player busy":
                self.api.do_send_player_cmd(f"execute \"{playerName}\" ~~~ tell @a[tag=omg] 取消")
                input = self.api.do_get_get_player_next_param_input(playerName, f"§e[挂机检测] §c请在§e30秒内§c计算并发送 §e{x}+{y} §c进行验证，否则服务器将会断开连接！")
            if input.input[0] == str(x+y):
                # 误触发不给补偿可不好（
                self.api.do_send_wo_cmd(f"scoreboard \"{playerName}\" players add money 200")
                self.api.do_send_player_msg(playerName, "§e[挂机检测] §a验证成功！已获得奖励: §9结晶碎片*200")
                return True
            else:
                chance-=1
                if chance > 0:
                    self.api.do_send_player_msg(playerName, f"§e[挂机检测] §c输入错误，还剩下 §e{chance}次 §c验证次数")
                else:
                    return False

    def verify(self, playerName):
        try:
            passed = self.verify_in_time(playerName)
        except func_timeout.exceptions.FunctionTimedOut:
            passed = False
        if not passed:
            self.kick(playerName)

    def deal_expire(self, dict):
        for k, v in dict.items():
            v.expire-=1
            if v.expire < 1:
                dict.pop(k)
        return dict

    # 精确检测，但是，寄！已被自动操作脚本击穿
    def detect_yRot(self):
        # 发送指令
        response = self.api.do_send_ws_cmd("querytarget @a[tag=!omg]")
        # 没有目标则不处理
        if response.result.OutputMessages[0].Success:
            for data in json.loads(response.result.OutputMessages[0].Parameters[0]):
                playerObj = player(UUID=data['uniqueId'], yRot=data['yRot'])
                # 即使不动也会有细微偏差，所以取2位小数; 以及会出现某种奇妙的情况; **网易
                if playerObj.UUID in self.dict_yRot.keys():
                    if round(playerObj.yRot, 2) == round(self.dict_yRot[playerObj.UUID].yRot, 2) or 359 < abs(playerObj.yRot)+abs(self.dict_yRot[playerObj.UUID].yRot) < 361:
                        playerObj.time = self.dict_yRot[playerObj.UUID].time + 1
                    if playerObj.time > random.randrange(15, 30):
                        self.api.execute_in_individual_thread(self.verify, self.api.get_player_name(playerObj.UUID))
                        playerObj.time = 0
                self.dict_yRot.update({data['uniqueId']: playerObj})
        # 更新过期时间
        self.dict_yRot = self.deal_expire(self.dict_yRot)
    
    # 并非精确检测，应配合验证码使用
    def detect_distance(self):
        # 发送指令
        response = self.api.do_send_ws_cmd("querytarget @a[tag=!omg]")
        # 没有目标则不处理
        if response.result.OutputMessages[0].Success:
            for data in json.loads(response.result.OutputMessages[0].Parameters[0]):
                playerObj = player(UUID=data['uniqueId'], posx=data['position']['x'], posz=data['position']['z'])
                if playerObj.UUID in self.dict_distance.keys():
                    if pow(pow(playerObj.posx-self.dict_distance[playerObj.UUID].posx, 2)+pow(playerObj.posz-self.dict_distance[playerObj.UUID].posz, 2), 0.5) < 200:
                        playerObj.time = self.dict_distance[playerObj.UUID].time + 1
                    if playerObj.time > random.randrange(15, 30):
                        self.api.execute_in_individual_thread(self.verify, self.api.get_player_name(playerObj.UUID))
                        playerObj.time = 0
                self.dict_distance.update({data['uniqueId']: playerObj})
        # 更新过期时间
        self.dict_distance = self.deal_expire(self.dict_distance)

    def __call__(self, API:API):
        # 获取API
        self.api=api(API)
        # 注册功能 - 请不要同时开启！！
        # self.api.execute_with_repeat(func=self.detect_yRot, repeat_time=60) # 没用了，抬走吧
        self.api.execute_with_repeat(func=self.detect_distance, repeat_time=60)

omega.add_plugin(plugin=plugin())
omega.run(addr=None)
