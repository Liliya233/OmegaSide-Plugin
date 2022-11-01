# 插件: 开
# Name：挂机检测
# Version：0.0.3
# Author：Liliya233
from typing import Callable
from omega_side.python3_omega_sync import API
from omega_side.python3_omega_sync import frame as omega
from omega_side.python3_omega_sync.bootstrap import install_lib
from omega_side.python3_omega_sync.protocol import *
from API_By_Liliya import api
import time
import json
import random

install_lib(lib_name="func_timeout",lib_install_name="func_timeout")
import func_timeout

class queryResult(object):
    def __init__(self, jsonData):
        # uuid
        self.uuid = jsonData['uniqueId']
        # 视角
        self.yRot = jsonData['yRot']
        # 维度
        self.dim = jsonData['dimension']
        # X轴坐标
        self.posx = jsonData['position']['x']
        # Y轴坐标
        self.posy = jsonData['position']['y']
        # Z轴坐标
        self.posz = jsonData['position']['z']

class player(object):
    def __init__(self, resultObj:queryResult, time=1, expire=120, fail=0, isVerifying=False):
        # UUID
        self.uuid = resultObj.uuid
        # 上次视角
        self.yRot = resultObj.yRot
        # 上次所在维度
        self.dim = resultObj.dim
        # 上次X轴坐标
        self.posx = resultObj.posx
        # 上次Y轴坐标
        self.posy = resultObj.posy
        # 上次Z轴坐标
        self.posz = resultObj.posz
        # 挂机时间
        self.time = time
        # 保存时间 - 玩家退出登录后，记录应被保存一段时间
        self.expire = expire
        # 连续验证失败次数
        self.fail = fail
        # 是否正在验证
        self.isVerifying = isVerifying

class plugin(object):
    def __init__(self):
        # 数据记录
        self.dict=dict()

    def punish(self, playerName):
        self.api.do_send_wo_cmd(f"tp \"{playerName}\" -3680 84 1917")
        self.api.do_send_player_msg(playerName, "§e[挂机检测] §c疑似长时间挂机，已将你传送至挂机池")

    @func_timeout.func_set_timeout(29)
    def verify_in_time(self, playerName):
        chance = 3
        while True:
            x = random.randrange(1, 25)
            y = random.randrange(1, 25)
            input = self.api.do_get_get_player_next_param_input(playerName, f"§e[挂机检测] §c请在§e30秒内§c计算并发送 §e{x}+{y} §c进行人机验证")
            if input.err == "player busy":
                self.api.do_send_ws_cmd(f"execute \"{playerName}\" ~~~ tell @a[tag=omg] 取消")
                input = self.api.do_get_get_player_next_param_input(playerName, f"§e[挂机检测] §c请在§e30秒内§c计算并发送 §e{x}+{y} §c进行人机验证")
            if input.input[0] == str(x+y):
                # 误触发不给补偿可不好（
                self.api.do_send_wo_cmd(f"scoreboard players add \"{playerName}\" money 200")
                self.api.do_send_player_msg(playerName, "§e[挂机检测] §a验证成功！已获得奖励:§9结晶碎片*200")
                return True
            else:
                chance-=1
                if chance > 0:
                    self.api.do_send_player_msg(playerName, f"§e[挂机检测] §c输入错误，还剩下 §e{chance}次 §c验证机会")
                else:
                    return False

    def verify(self, playerObj:player):
        playerObj.isVerifying = True
        playerName = self.api.get_player_name(playerObj.uuid)
        try:
            passed = self.verify_in_time(playerName)
        except func_timeout.exceptions.FunctionTimedOut:
            passed = False
        if passed:
            playerObj.fail = 0
            playerObj.time = 0
        else:
            # 设置为上限值，符合检测要求将会立即触发验证，以防止自动脚本
            playerObj.time = 45
            playerObj.fail+=1
            self.punish(playerName)
            if playerObj.fail > 5:
                # 当然，可以在多次验证失败后加入额外的操作，由于暂时不需要就将它注释掉了
                # 连续被踢出5次以上，交由Omega执行临时封禁
                #self.api.do_send_wo_cmd(f"scoreboard players add \"{playerName}\" ban 2100")
                pass
        playerObj.isVerifying = False

    def deal_expire(self):
        for k in list(self.dict.keys()):
            self.dict[k].expire-=1
            if self.dict[k].expire < 1:
                self.dict.pop(k)

    # 检测方法 - 视角对比 - 精确检测，但是，寄！已被自动操作脚本击穿
    def detect_yRot(self, playerObj:player, resultObj:queryResult):
        return round(resultObj.yRot, 2) == round(playerObj.yRot, 2) or 359 < abs(resultObj.yRot)+abs(playerObj.yRot) < 361

    # 检测方法 - 距离对比 - 并非精确检测，应配合验证码使用
    def detect_distance(self, playerObj:player, resultObj:queryResult):
        return pow(pow(resultObj.posx-playerObj.posx, 2)+pow(resultObj.posz-playerObj.posz, 2), 0.5) < 200

    # 检测方法 - 全部检测 - 无差别打击！
    def detect_all(self, playerObj:player, resultObj:queryResult):
        return True

    def detect(self, detectFunc:Callable):
        # 随机延迟一段时间
        time.sleep(random.randrange(1, 30))
        # 发送指令
        response = self.api.do_send_ws_cmd("querytarget @a[tag=!omg]")
        # 没有目标则不处理
        if response.result.OutputMessages[0].Success:
            for data in json.loads(response.result.OutputMessages[0].Parameters[0]):
                resultObj = queryResult(data)
                if resultObj.uuid in self.dict.keys():
                    playerObj:player = self.dict[resultObj.uuid]
                    # PS: 玩家不处于验证状态且玩家不在挂机池范围内
                    if not playerObj.isVerifying and not (resultObj.dim == 0 and self.api.get_distance(resultObj.posx, resultObj.posy, resultObj.posz, -3680, 84, 1917) < 30):
                        if detectFunc(playerObj, resultObj):
                            playerObj.time += 1
                        if playerObj.time > random.randrange(30, 45):
                            self.api.execute_in_individual_thread(self.verify, playerObj)
                else:
                    playerObj = player(resultObj)
                self.dict.update({playerObj.uuid: playerObj})
        # 更新过期时间
        self.deal_expire()

    def __call__(self, API:API):
        # 获取API
        self.api=api(API)
        # 注册功能 - 应在此选择一个检测函数
        self.api.execute_with_repeat(self.detect, self.detect_distance, repeat_time=60)

omega.add_plugin(plugin=plugin())
omega.run(addr=None)
