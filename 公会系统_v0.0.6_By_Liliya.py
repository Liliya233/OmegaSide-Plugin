# 插件: 开
import json
import time
from omega_side.python3_omega_sync import API
from omega_side.python3_omega_sync import frame as omega
from omega_side.python3_omega_sync.protocol import *
from API_By_Liliya import api

# 变量类
class param:
    guildDict = {}

# 玩家实体类
class player:
    def __init__(self, UUID='', name='', power=0, contribute=0):
        # UUID
        self.UUID = UUID
        # 昵称
        self.name = name
        # 权限等级
        self.power = power
        # 贡献值
        self.contribute = contribute

    # 通过UUID查询玩家对象
    def getByUUID(UUID):
        guildObj = guild.getByUUID(UUID)
        if guildObj:
            playerObj = player()
            playerObj.__dict__ = guildObj.members[UUID]
            return playerObj
        return False

    # 通过UUID查询玩家公会权限
    def getPowerByUUID(UUID):
        playerObj = player.getByUUID(UUID)
        if playerObj:
            return player.getByUUID(UUID).power
        return False

    # 根据贡献值进行玩家排序
    def sort(members):
        return dict(sorted(members.items(), key=lambda x: x[1]['contribute'], reverse=True))

# 公会实体类
class guild:
    def __init__(self, name='', level=1, contribute=0, president='', isClosed=False, pos={'d':0, 'x':0, 'y':0, 'z':0}, members={}):
        # 昵称
        self.name = name
        # 等级
        self.level = level
        # 贡献值
        self.contribute = contribute
        # 是否禁入
        self.isClosed = isClosed
        # 会长UUID
        self.president = president
        # 中心坐标
        self.pos = pos
        # 会员列表
        self.members = members

    # 新增一个公会
    def add(guild):
        if guild.name not in param.guildDict:
            param.guildDict.update({guild.name: guild.__dict__})
            tool.writeToFile(param.guildDict)
            return True
        return False

    # 更新一个公会
    def update(guild):
        if guild.name in param.guildDict:
            param.guildDict.update({guild.name: guild.__dict__})
            tool.writeToFile(param.guildDict)
            return True
        return False

    # 删除一个公会
    def delete(guildName):
        if guildName in param.guildDict:
            param.guildDict.pop(guildName)
            tool.writeToFile(param.guildDict)
            return True
        return False

    # 通过公会昵称获取公会对象
    def getByName(guildName):
        if guildName in param.guildDict:
            guildObj = guild()
            guildObj.__dict__ = param.guildDict[guildName]
            return guildObj
        return False

    # 通过玩家UUID获取其归属的公会对象
    def getByUUID(playerUUID):
        for gkey in param.guildDict.keys():
            if playerUUID in param.guildDict[gkey]['members'].keys():
                    return guild.getByName(gkey)
        return False

    # 通过坐标信息获取公会对象
    def getByPos(pos):
        for gkey, gdata in param.guildDict.items():
            # 根据公会等级设定范围
            if gdata['level'] == 4: dx = 400
            elif gdata['level'] == 3: dx = 300
            elif gdata['level'] == 2: dx = 200
            else: dx = 150
            # 判断
            if pos['d'] == gdata['pos']['d'] and (gdata['pos']['x']-dx)<=pos['x']<=(gdata['pos']['x']+dx) and (gdata['pos']['z']-dx)<=pos['z']<=(gdata['pos']['z']+dx):
                return guild.getByName(gkey)
        return False
    
    # 获取指定公会的玩家列表，type: 0=全部玩家 1=正式会员 2=未审核会员
    def getMembers(guildName, type):
        result=[]
        if type==0:
            for data in param.guildDict[guildName]['members'].values():
                result.append(data)
        elif type==1:
            for data in param.guildDict[guildName]['members'].values():
                if data['power'] > 0:
                    result.append(data)
        elif type==2:
            for data in param.guildDict[guildName]['members'].values():
                if data['power'] == 0:
                    result.append(data)
        return result

    # 获取最近的公会边界
    def getBoard(guild, pos):
        # 根据公会等级设定范围
        if guild.level == 4: dx = 402
        elif guild.level == 3: dx = 302
        elif guild.level == 2: dx = 202
        else: dx = 152
        # 计算玩家坐标与公会左下角坐标差绝对值
        x = pos['x'] - guild.pos['x'] + dx
        z = pos['z'] - guild.pos['z'] + dx
        # 判断
        if z<=2*dx-x:
            if z<=x:
                pos['z'] = guild.pos['z'] - dx
            else:
                pos['x'] = guild.pos['x'] - dx
        else:
            if z<=x:
                pos['x'] = guild.pos['x'] + dx
            else:
                pos['z'] = guild.pos['z'] + dx
        # 返回
        return pos

    # 获取玩家所属公会的等级
    def getLevelByUUID(UUID):
        guildObj = guild.getByUUID(UUID)
        if guildObj:
            return guildObj['level']
        return False

    # 通过坐标信息查询附件是否存在其他公会
    def hasGuildNearby(pos):
        for gdata in param.guildDict.values():
            # 判断
            if pos['d'] == gdata['pos']['d'] and (gdata['pos']['x']-900)<=pos['x']<=(gdata['pos']['x']+900) and (gdata['pos']['z']-900)<=pos['z']<=(gdata['pos']['z']+900):
                return True
        return False

    # 根据等级与贡献值进行公会排序
    def sort():
        return dict(sorted(param.guildDict.items(), key=lambda x: (x[1]['level'], x[1]['contribute']), reverse=True))

# 工具类
class tool:
    # 路径
    path = './data/公会系统_By_Liliya.json'
 
    # 输出数据到JSON文件
    def writeToFile(dict):
        with open(tool.path, 'w', encoding='utf-8') as file:
            json.dump(dict, file, indent=4, ensure_ascii=False)

    # 从JSON文件读取数据
    def readFromFile():
        try:
            with open(tool.path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception:
            return {}

# 公会插件
class guildPlugin(object):
    def __init__(self, name:str="公会系统") -> None:
        self.name=name

    # 菜单项-返回公会
    def menu_back(self, input:PlayerInput):
        playerName = input.Name
        UUID = self.api.get_player_uuid(playerName)
        # 是否拥有公会
        if player.getPowerByUUID(UUID) in [False, 0]:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法使用此功能，你当前未加入任何公会哦！")
            return
        # 获取公会
        guildObj = guild.getByUUID(UUID)
        # 发送传送指令
        self.api.do_send_wo_cmd(f"tp @a[name=\"{playerName}\"] {guildObj.pos['x']} {guildObj.pos['y']} {guildObj.pos['z']}")
        self.api.do_send_player_msg(playerName, f"§e[公会系统] §b欢迎回到公会 - §e{guildObj.name}")
    
    # 菜单项-贡献
    def menu_contribute(self, input:PlayerInput):
        playerName = input.Name
        UUID = self.api.get_player_uuid(playerName)
        try:
            # 要求玩家输入贡献数量
            count = int(self.api.do_get_get_player_next_param_input(playerName, hint="§e[公会系统] §b请输入需要贡献的数量：").input[0])
        except Exception:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c只能输入数字哦！")
            return
        # 数值检测
        if count < 1:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c只能输入大于0的数字哦！")
            return
        # 是否拥有公会
        if player.getPowerByUUID(UUID) in [False, 0]:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法使用此功能，你当前未加入任何公会哦！")
            return
        # 判断是否扣费成功
        if not self.api.add_player_score(playerName, 'money', -count):
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c贡献失败！请确保你有足够的余额哦！")
            return
        # 获取公会
        guildObj = guild.getByUUID(UUID)
        # 增加贡献
        guildObj.contribute += count
        guildObj.members[UUID]['contribute'] += count
        # 存储写入
        guild.update(guildObj)
        self.api.do_send_player_msg(playerName, "§e[公会系统] §a感谢你为公会作出的贡献~")

    # 菜单项-公会信息
    def menu_info(self, input:PlayerInput):
        playerName = input.Name
        UUID = self.api.get_player_uuid(playerName)
        # 是否拥有公会
        if player.getPowerByUUID(UUID) in [False, 0]:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法使用此功能，你当前未加入任何公会哦！")
            return
        # 获取公会
        guildObj = guild.getByUUID(UUID)
        # 打印信息
        self.api.do_send_player_msg(playerName, "§l§aGUILD INFO - §b公会信息")
        self.api.do_send_player_msg(playerName, f"§g公会名称 §b- §a{guildObj.name}")
        self.api.do_send_player_msg(playerName, f"§g会长昵称 §b- §a{guildObj.members[guildObj.president]['name']}")
        self.api.do_send_player_msg(playerName, f"§g公会等级 §b- §a{guildObj.level}")
        self.api.do_send_player_msg(playerName, f"§g公会贡献 §b- §a{guildObj.contribute}")
        self.api.do_send_player_msg(playerName, f"§g公会坐标 §b- §a({guildObj.pos['x']}, {guildObj.pos['y']}, {guildObj.pos['z']})")
        self.api.do_send_player_msg(playerName, f"§g禁入状态 §b- §a{'§c启用' if guildObj.isClosed else '§a禁用'}")
        self.api.do_send_player_msg(playerName, "§l§aGUILD INFO - §b会员列表")
        rank=0
        for data in player.sort(guildObj.members).values():
            if data['power'] > 0:
                rank+=1
                if data['power'] == 1:
                    self.api.do_send_player_msg(playerName, f"§l§6{rank}.§r§e{data['name']} §b- §7普通会员 §b- §9贡献*{data['contribute']}")
                elif data['power'] == 2:
                    self.api.do_send_player_msg(playerName, f"§l§6{rank}.§r§e{data['name']} §b- §d高级会员 §b- §9贡献*{data['contribute']}")
                elif data['power'] == 3:
                    self.api.do_send_player_msg(playerName, f"§l§6{rank}.§r§e{data['name']} §b- §a公会管理 §b- §9贡献*{data['contribute']}")
                elif data['power'] == 4:
                    self.api.do_send_player_msg(playerName, f"§l§6{rank}.§r§e{data['name']} §b- §6公会会长 §b- §9贡献*{data['contribute']}")
        self.api.do_send_player_msg(playerName, "§l§aGUILD INFO - 显示完毕")

    # 菜单项-公会列表与功能
    def menu_list(self, input:PlayerInput):
        playerName = input.Name
        UUID = self.api.get_player_uuid(playerName)
        # 打印头部
        self.api.do_send_player_msg(playerName, "§l§aGUILD INFO - §b公会信息")
        # 打印列表
        rank=0
        guildNameList=[]
        for data in guild.sort().values():
            rank+=1
            self.api.do_send_player_msg(playerName, f"§l§6{rank} §r§b公会名：§e{data['name']} §b- 等级：§a{data['level']}级 §b- 当前贡献：§9{data['contribute']} §b- 会长：§6{data['members'][data['president']]['name']}")
            guildNameList.append(data['name'])
        # 打印尾部
        self.api.do_send_player_msg(playerName, "§l§aGUILD INFO - §d请根据下方提示进行输入")
        # 获取玩家选择
        try:
            select_1 = int(self.api.do_get_get_player_next_param_input(playerName, hint="§e[公会系统] §b请输入一个公会编号，进行下一步操作：").input[0])
        except Exception:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c只能输入编号哦！")
            return
        # 判断是否越界
        if not 0 < select_1 <= len(guildNameList):
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c不存在这个选项哦！")
            return
        # 打印头部
        self.api.do_send_player_msg(playerName, "§l§aGUILD INFO - §b公会菜单")
        self.api.do_send_player_msg(playerName, f"§7当前已选中公会：§e{guildNameList[select_1-1]}")
        # 打印选项列表
        self.api.do_send_player_msg(playerName, "§l§61 §eapply §r§b向该公会发送入会申请")
        self.api.do_send_player_msg(playerName, "§l§62 §equery §r§e[仅OP]§b查询该公会的详情信息")
        self.api.do_send_player_msg(playerName, "§l§63 §eteleport §r§e[仅OP]§b传送至该公会中心")
        self.api.do_send_player_msg(playerName, "§l§64 §eremove §r§e[仅OP]§b强制移除该公会")
        # 打印尾部
        self.api.do_send_player_msg(playerName, "§l§aGUILD INFO - §d请根据下方提示进行输入")
        # 获取玩家选择
        select_2 = self.api.do_get_get_player_next_param_input(playerName, hint="§e[公会系统] §b请输入一个公会编号，进行下一步操作：").input[0]
        # 功能项
        if select_2 in ['1', 'apply']:
            # 查询玩家是否有公会
            power = player.getPowerByUUID(UUID)
            if power > 0:
                self.api.do_send_player_msg(playerName, "§e[公会系统] §c你已经加入一个公会啦！")
                return
            # 若处于申请状态，则撤销
            if power is not False and power == 0:
                guildObj = guild.getByUUID(UUID)
                guildObj.members.pop(UUID)
                guild.update(guildObj)
            # 将玩家存入选中公会
            guildObj = guild.getByName(guildNameList[select_1-1])
            guildObj.members.update({UUID: player(UUID=UUID, name=playerName).__dict__})
            guild.update(guildObj)
            # 提示
            self.api.do_send_player_msg(playerName, "§e[公会系统] §a申请成功！请等待公会管理员进行审核！")
        elif select_2 in ['2', 'query']:
            if self.api.get_player_permission(playerName) != "操作员":
                self.api.do_send_player_msg(playerName, "§e[公会系统] §c当前选项仅OP可使用哦！")
                return
            # 获取公会对象
            guildObj = guild.getByName(guildNameList[select_1-1])
            # 打印信息
            self.api.do_send_player_msg(playerName, "§l§aGUILD INFO - §b公会信息")
            self.api.do_send_player_msg(playerName, f"§g公会名称 §b- §a{guildObj.name}")
            self.api.do_send_player_msg(playerName, f"§g会长昵称 §b- §a{guildObj.members[guildObj.president]['name']}")
            self.api.do_send_player_msg(playerName, f"§g公会等级 §b- §a{guildObj.level}")
            self.api.do_send_player_msg(playerName, f"§g公会贡献 §b- §a{guildObj.contribute}")
            self.api.do_send_player_msg(playerName, f"§g公会坐标 §b- §a({guildObj.pos['x']}, {guildObj.pos['y']}, {guildObj.pos['z']})")
            self.api.do_send_player_msg(playerName, f"§g禁入状态 §b- §a{'§c启用' if guildObj.isClosed else '§a禁用'}")
            self.api.do_send_player_msg(playerName, "§l§aGUILD INFO - §b会员列表")
            rank=0
            for data in player.sort(guildObj.members).values():
                if data['power'] > 0:
                    rank+=1
                    if data['power'] == 1:
                        self.api.do_send_player_msg(playerName, f"§l§6{rank}.§r§e{data['name']} §b- §7普通会员 §b- §9贡献*{data['contribute']}")
                    elif data['power'] == 2:
                        self.api.do_send_player_msg(playerName, f"§l§6{rank}.§r§e{data['name']} §b- §d高级会员 §b- §9贡献*{data['contribute']}")
                    elif data['power'] == 3:
                        self.api.do_send_player_msg(playerName, f"§l§6{rank}.§r§e{data['name']} §b- §a公会管理 §b- §9贡献*{data['contribute']}")
                    elif data['power'] == 4:
                        self.api.do_send_player_msg(playerName, f"§l§6{rank}.§r§e{data['name']} §b- §6公会会长 §b- §9贡献*{data['contribute']}")
            self.api.do_send_player_msg(playerName, "§l§aGUILD INFO - 显示完毕")
        elif select_2 in ['3', 'teleport']:
            if self.api.get_player_permission(playerName) != "操作员":
                self.api.do_send_player_msg(playerName, "§e[公会系统] §c当前选项仅OP可使用哦！")
                return
            # 获取公会对象
            guildObj = guild.getByName(guildNameList[select_1-1])
            # 传送
            self.api.do_send_wo_cmd(f"tp {playerName} {guildObj.pos['x']} {guildObj.pos['y']} {guildObj.pos['z']}")
            self.api.do_send_player_msg(playerName, "§e[公会系统] §a已将你传送至目标公会！")
        elif select_2 in ['4', 'remove']:
            if self.api.get_player_permission(playerName) != "操作员":
                self.api.do_send_player_msg(playerName, "§e[公会系统] §c当前选项仅OP可使用哦！")
                return
            # 移除公会
            if self.api.do_get_get_player_next_param_input(playerName, hint="§e[公会系统] §b若要移除公会，请输入§e确认§b继续进行该操作(§d确认后不可撤销§b)：").input[0] == '确认':
                guild.delete(guildNameList[select_1-1])
                self.api.do_send_player_msg(playerName, f"§e[公会系统] §a已成功移除：§e{guildNameList[select_1-1]}")
            else:
                self.api.do_send_player_msg(playerName, "§e[公会系统] §c确认失败！本次操作已中断！")
        else:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c不存在这个选项哦！")

    # 菜单项-创建公会
    def menu_create(self, input:PlayerInput):
        playerName = input.Name
        UUID = self.api.get_player_uuid(playerName)
        # 要求玩家输入公会名
        guildName = self.api.do_get_get_player_next_param_input(playerName, hint="§e[公会系统] §b请为公会起个名字吧！(§e不能输入空格哦§b)：").input[0]
        # 判断是否重名
        if guild.getByName(guildName):
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c这个名字已经被使用啦！")
            return
        # 判断是否已加入公会
        if guild.getByUUID(UUID) and player.getPowerByUUID(UUID) > 0:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c你当前已经加入一个公会了，不能进行创建哦！")
            return
        # 判断是否符合选择器
        if self.api.do_send_ws_cmd(f"testfor @a[name=\"{playerName}\",m=!a,scores={{ID=1..,dim=1}},tag=!保护区域]").result.SuccessCount < 1:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c创建失败！请确保你当前位于主世界资源区哦！")
            return
        # 判断附件是否存在公会
        if guild.hasGuildNearby(self.api.get_player_pos(playerName)):
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c创建失败！附近存在其他公会！")
            return
        # 判断是否扣费成功
        if not self.api.add_player_score(playerName, 'money', -500000):
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c创建失败！请确保你有足够的余额哦！")
            return
        # 新建玩家对象
        playerObj = player(UUID=UUID, name=playerName, power=4)
        # 新建会员字典
        membersDict = {}
        membersDict.update({playerObj.UUID: playerObj.__dict__})
        # 新建公会对象
        guildObj = guild(name=guildName, pos=self.api.get_player_pos(UUID), members=membersDict, president=UUID)
        # 存储写入
        guild.add(guildObj)
        # 提示
        self.api.do_send_player_msg(playerName, "§e[公会系统] §a创建成功！快邀请其他小伙伴加入公会吧！")
        # 更新分数
        self.api.set_player_score(playerName, "guildLevel", 1)

    # 菜单项-公会商店
    def menu_mall(self, input:PlayerInput):
        # 获取玩家信息
        playerName = input.Name
        UUID = self.api.get_player_uuid(playerName)
        guildObj = guild.getByUUID(UUID)
        # 判断是否拥有公会
        if guildObj:
            # 同步计分板
            self.api.set_player_score(playerName, "guildLevel", guildObj.level)
            if guildObj.level >= 2:
                self.api.do_send_wo_cmd(f"execute @a[name=\"{playerName}\"] ~~~ tell @a[tag=omg] +gmall-exec")
                self.api.do_send_wo_cmd(f"execute @a[name=\"{playerName}\"] ~~~ tell @a[tag=omg] 1")
                self.api.execute_after(func=lambda:self.api.do_send_player_msg(playerName, '§e[公会系统] §b请输入§e[物品序号] [购买数量]§b来进行批量购买吧~'), delay_time=1)
                return
        self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法使用此功能，只有2级或以上公会的会员才能使用哦！")

    # 菜单项-退出公会
    def menu_leave(self, input:PlayerInput):
        playerName = input.Name
        UUID = self.api.get_player_uuid(playerName)
        # 是否拥有公会
        if player.getPowerByUUID(UUID) in [False, 0]:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法使用此功能，你当前未加入任何公会哦！")
            return
        # 获取公会
        guildObj = guild.getByUUID(UUID)
        # 是否会长
        if UUID == guildObj.president:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c会长不能退出公会哦！")
            return
        if self.api.do_get_get_player_next_param_input(playerName, hint="§e[公会系统] §b若要退出公会，请输入§e确认§b继续进行该操作(§d确认后不可撤销§b)：").input[0] == '确认':
            # 删除会员
            guildObj.members.pop(UUID)
            # 存储写入
            guild.update(guildObj)
            self.api.do_send_player_msg(playerName, "§e[公会系统] §a你已成功退出当前公会！")
            # 更新分数
            self.api.set_player_score(playerName, "guildLevel", 0)
        else:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c确认失败！本次操作已中断！")

    # 管理菜单项-升级公会
    def menu_upgrade(self, input:PlayerInput):
        playerName = input.Name
        UUID = self.api.get_player_uuid(playerName)
        # 权限验证
        if player.getPowerByUUID(UUID) in [False, 0, 1]:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法使用此功能，公会权限需要达到§d高级会员§c或以上")
            return
        # 获取公会对象
        guildObj = guild.getByUUID(UUID)
        # 等级上限
        if not guildObj.level < 4:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §a公会已达到最高等级，无需继续升级啦！")
            return
        # 尝试扣除贡献
        if not guildObj.contribute >= 500000:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c升级失败，公会贡献不足！")
            return
        guildObj.contribute -= 500000
        guildObj.level+=1
        # 存储写入
        guild.update(guildObj)
        self.api.do_send_player_msg(playerName, f"§e[公会系统] §a升级成功！当前公会等级为：§e{guildObj.level}级")
        # 更新分数
        for data in guildObj.members.values():
            self.api.set_player_score(data['name'], "guildLevel", guildObj.level)

    # 管理菜单项-公会禁入
    def menu_close(self, input:PlayerInput):
        playerName = input.Name
        UUID = self.api.get_player_uuid(playerName)
        # 权限验证
        if player.getPowerByUUID(UUID) in [False, 0, 1, 2]:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法使用此功能，公会权限需要达到§a公会管理§c或以上")
            return
        # 获取公会对象
        guildObj = guild.getByUUID(UUID)
        # 状态更新
        if guildObj.isClosed:
            guildObj.isClosed = False
        else:
            guildObj.isClosed = True
        # 存储写入
        guild.update(guildObj)
        self.api.do_send_player_msg(playerName, f"§e[公会系统] §a更改成功！当前公会禁入设置为：§e{'§c启用' if guildObj.isClosed else '§a禁用'}")

    # 管理菜单项-人员管理
    def menu_manger(self, input:PlayerInput):
        playerName = input.Name
        UUID = self.api.get_player_uuid(playerName)
        # 权限验证
        if player.getPowerByUUID(UUID) in [False, 0, 1]:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法使用此功能，公会权限需要达到§a公会管理§c或以上")
            return
        guildObj = guild.getByUUID(UUID)
        # 列出会员
        self.api.do_send_player_msg(playerName, "§l§aGUILD MANAGE - §b会员管理")
        rank=0
        playerUUIDList=[]
        for data in player.sort(guildObj.members).values():
            if data['power'] > 0:
                rank+=1
                if data['power'] == 1:
                    self.api.do_send_player_msg(playerName, f"§l§6{rank}.§r§e{data['name']} §b- §7普通会员 §b- §9贡献*{data['contribute']}")
                elif data['power'] == 2:
                    self.api.do_send_player_msg(playerName, f"§l§6{rank}.§r§e{data['name']} §b- §d高级会员 §b- §9贡献*{data['contribute']}")
                elif data['power'] == 3:
                    self.api.do_send_player_msg(playerName, f"§l§6{rank}.§r§e{data['name']} §b- §a公会管理 §b- §9贡献*{data['contribute']}")
                elif data['power'] == 4:
                    self.api.do_send_player_msg(playerName, f"§l§6{rank}.§r§e{data['name']} §b- §6公会会长 §b- §9贡献*{data['contribute']}")
                playerUUIDList.append(data['UUID'])
        self.api.do_send_player_msg(playerName, "§l§aGUILD MANAGE - §d请根据下方提示进行输入")
        # 获取玩家选择
        try:
            select_1 = int(self.api.do_get_get_player_next_param_input(playerName, hint="§e[公会系统] §b请输入一个玩家编号，进行下一步操作：").input[0])
        except Exception:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c只能输入编号哦！")
            return
        # 判断是否越界
        if not 0 < select_1 <= len(playerUUIDList):
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c不存在这个选项哦！")
            return
        # 打印头部
        self.api.do_send_player_msg(playerName, "§l§aGUILD MANAGE - §b会员管理")
        self.api.do_send_player_msg(playerName, f"§7当前已选中会员：§e{player.getByUUID(playerUUIDList[select_1-1]).name}")
        # 打印选项列表
        self.api.do_send_player_msg(playerName, "§l§61 §eremove §r§e[§a公会管理§e+]§b将该名会员移出公会")
        self.api.do_send_player_msg(playerName, "§l§62 §esetpower §r§e[§6公会会长§e]§b设置该名会员的权限")
        # 打印尾部
        self.api.do_send_player_msg(playerName, "§l§aGUILD MANAGE - §d请根据下方提示进行输入")
        # 获取玩家选择
        select_2 = self.api.do_get_get_player_next_param_input(playerName, hint="§e[公会系统] §b请输入一个选项编号，进行下一步操作：").input[0]
        # 功能项
        if select_2 in ['1', 'remove']:
            # 权限验证
            if player.getPowerByUUID(UUID) in [False, 0, 1, 2]:
                self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法使用此功能，公会权限需要达到§a公会管理§c或以上")
                return
            # 权限对比
            if player.getPowerByUUID(UUID) == 3 and player.getPowerByUUID(playerUUIDList[select_1-1]) > 2:
                self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法移除，当前权限等级仅允许移除§7普通会员§c与§d高级会员")
                return
            if player.getPowerByUUID(UUID) == 4 and player.getPowerByUUID(playerUUIDList[select_1-1]) > 3:
                self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法移除，当前权限等级仅允许移除§7普通会员§c、§d高级会员§c与§a公会管理")
                return
            # 更新分数
            self.api.set_player_score(player.getByUUID(playerUUIDList[select_1-1]).name, "guildLevel", 0)
            # 移除会员
            guildObj.members.pop(playerUUIDList[select_1-1])
            # 存储写入
            guild.update(guildObj)
            self.api.do_send_player_msg(playerName, "§e[公会系统] §a已成功将该会员移出公会！")
        elif select_2 in ['2', 'setpower']:
            # 权限验证
            if player.getPowerByUUID(UUID) in [False, 0, 1, 2, 3]:
                self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法使用此功能，公会权限需要达到§6公会会长")
                return
            # 权限对比
            if player.getPowerByUUID(playerUUIDList[select_1-1]) > 3:
                self.api.do_send_player_msg(playerName, "§e[公会系统] §c会长权限不允许更改哦！")
                return
            # 打印头部
            self.api.do_send_player_msg(playerName, "§l§aGUILD MANAGE - §b会员管理")
            self.api.do_send_player_msg(playerName, f"§7当前已选中会员：§e{player.getByUUID(playerUUIDList[select_1-1]).name}")
            # 打印选项列表
            self.api.do_send_player_msg(playerName, "§l§61 §eordinary §r§b将该名会员的权限设置为§7普通会员")
            self.api.do_send_player_msg(playerName, "§l§62 §esenior §r§b将该名会员的权限设置为§d高级会员")
            self.api.do_send_player_msg(playerName, "§l§63 §emanagement §r§b将该名会员的权限设置为§a公会管理")
            # 打印尾部
            self.api.do_send_player_msg(playerName, "§l§aGUILD MANAGE - §d请根据下方提示进行输入")
            # 获取玩家选择
            select_3 = self.api.do_get_get_player_next_param_input(playerName, hint="§e[公会系统] §b请输入要设置的权限：").input[0]
            pl = player.getByUUID(playerUUIDList[select_1-1])
            if select_3 in ['1', 'ordinary']:
                pl.power = 1
            elif select_3 in ['2', 'senior']:
                pl.power = 2
            elif select_3 in ['3', 'management']:
                pl.power = 3
            else:
                self.api.do_send_player_msg(playerName, "§e[公会系统] §c不存在这个选项哦！")
                return
            guildObj.members.update({pl.UUID: pl.__dict__})
            # 存储写入
            guild.update(guildObj)
            self.api.do_send_player_msg(playerName, "§e[公会系统] §a已成功更改该名会员的权限！")
        else:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c不存在这个选项哦！")

    # 管理菜单项-人员审批
    def menu_verify(self, input:PlayerInput):
        playerName = input.Name
        UUID = self.api.get_player_uuid(playerName)
        # 权限验证
        if player.getPowerByUUID(UUID) in [False, 0, 1]:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法使用此功能，公会权限需要达到§a公会管理§c或以上")
            return
        guildObj = guild.getByUUID(UUID)
        # 列出待审核会员
        self.api.do_send_player_msg(playerName, "§l§aGUILD VERIFY - §b会员审批")
        rank=0
        playerUUIDList=[]
        for data in player.sort(guildObj.members).values():
            if data['power'] == 0:
                rank+=1
                self.api.do_send_player_msg(playerName, f"§l§6{rank}.§r§e{data['name']} §b- §c等待审批")
                playerUUIDList.append(data['UUID'])
        self.api.do_send_player_msg(playerName, "§l§aGUILD VERIFY - §d请根据下方提示进行输入")
        # 获取玩家选择
        try:
            select_1 = int(self.api.do_get_get_player_next_param_input(playerName, hint="§e[公会系统] §b请输入一个玩家编号，进行下一步操作：").input[0])
        except Exception:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c只能输入编号哦！")
            return
        # 判断是否越界
        if not 0 < select_1 <= len(playerUUIDList):
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c不存在这个选项哦！")
            return
        # 打印头部
        self.api.do_send_player_msg(playerName, "§l§aGUILD VERIFY - §b会员审批")
        self.api.do_send_player_msg(playerName, f"§7当前已选中玩家：§e{player.getByUUID(playerUUIDList[select_1-1]).name}")
        # 打印选项列表
        self.api.do_send_player_msg(playerName, "§l§61 §eallow §r§b同意该入会申请")
        self.api.do_send_player_msg(playerName, "§l§62 §edeny §r§b拒绝该入会申请")
        # 打印尾部
        self.api.do_send_player_msg(playerName, "§l§aGUILD VERIFY - §d请根据下方提示进行输入")
        # 获取玩家选择
        select_2 = self.api.do_get_get_player_next_param_input(playerName, hint="§e[公会系统] §b请输入一个选项编号，进行下一步操作：").input[0]
        # 功能项
        pl = player.getByUUID(playerUUIDList[select_1-1])
        if select_2 in ['1', 'allow']:
            pl.power = 1
            guildObj.members.update({pl.UUID: pl.__dict__})
            self.api.do_send_player_msg(playerName, "§e[公会系统] §a你同意了该入会申请！")
            # 更新分数
            self.api.set_player_score(player.getByUUID(playerUUIDList[select_1-1]).name, "guildLevel", guildObj.level)
        elif select_2 in ['2', 'deny']:
            guildObj.members.pop(pl.UUID)
            self.api.do_send_player_msg(playerName, "§e[公会系统] §a你拒绝了该入会申请！")
        else:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c不存在这个选项哦！")
            return
        # 存储写入
        guild.update(guildObj)

    # 管理菜单项-公会解散
    def menu_dissolution(self, input:PlayerInput):
        playerName = input.Name
        UUID = self.api.get_player_uuid(playerName)
        # 权限验证
        if player.getPowerByUUID(UUID) in [False, 0, 1, 2, 3]:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法使用此功能，公会权限需要达到§6公会会长")
            return
        # 获取公会对象
        guildObj = guild.getByUUID(UUID)
        # 再次确认
        if self.api.do_get_get_player_next_param_input(playerName, hint="§e[公会系统] §b若要解散公会，请输入§e立即解散§b继续进行该操作(§d确认后不可撤销§b)：").input[0] == '立即解散':
            # 更新分数
            for data in guildObj.members.values():
                self.api.set_player_score(player.getByUUID(data['name']), "guildLevel", 0)
            # 解散公会
            guild.delete(guildObj.name)
            self.api.do_send_player_msg(playerName, "§e[公会系统] §a你已成功解散当前公会！")
        else:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c确认失败！本次操作已中断！")

    # 定时执行公会保护
    def protect(self):
        while True:
            # 循环间隔
            time.sleep(2)
            # 发送指令
            response = self.api.do_send_ws_cmd("querytarget @a[tag=!omg,tag=!保护区域]")
            try:
                # 解析
                for data in json.loads(response.result.OutputMessages[0].Parameters[0]):
                    # 解析
                    playerUUID = data['uniqueId']
                    playerName = self.api.get_player_name(playerUUID)
                    playerPos = {}
                    playerPos.update({"d": data['dimension']})
                    playerPos.update({"x": int(data['position']['x'])})
                    playerPos.update({"y": int(data['position']['y'])})
                    playerPos.update({"z": int(data['position']['z'])})
                    # 尝试获取公会
                    guildObj_1 = guild.getByPos(playerPos)
                    guildObj_2 = guild.getByUUID(playerUUID)
                    # 判断
                    if guildObj_1:
                        # 通用
                        self.api.do_send_wo_cmd(f"title @a[name=\"{playerName}\",scores={{menu=0}}] actionbar §b当前位于公会区域 - §e{guildObj_1.name}")
                        self.api.do_send_wo_cmd(f"tag @a[name=\"{playerName}\"] add 公会区域")
                        # 不为自己公会
                        if player.getPowerByUUID(playerUUID) in [False, 0] or guildObj_1.name != guildObj_2.name:
                            if guildObj_1.isClosed:
                                board = guild.getBoard(guildObj_1, playerPos)
                                self.api.do_send_wo_cmd(f"tp @a[name=\"{playerName}\",m=!c] {board['x']} {board['y']} {board['z']}")
                                self.api.do_send_wo_cmd(f"titleraw @a[name=\"{playerName}\",m=!c] actionbar {{\"rawtext\":[{{\"text\":\"§c当前公会不允许非公会成员进入\"}}]}}")
                            else:
                                self.api.do_send_wo_cmd(f"gamemode a @a[name=\"{playerName}\",m=s]")
                        else:
                            if guildObj_1.members[playerUUID]['name'] != playerName:
                                guildObj_1.members[playerUUID]['name'] = playerName
                                guild.update(guildObj_1)
                    else:
                        self.api.do_send_wo_cmd(f"title @a[name=\"{playerName}\",scores={{menu=0}},tag=公会区域] actionbar §b已离开公会区域")
                        self.api.do_send_wo_cmd(f"tag @a[name=\"{playerName}\",tag=公会区域] remove 公会区域")
            except Exception:
                pass

    def __call__(self, API:API):
        # 获取API
        self.api=api(API)
        # 读取公会信息
        param.guildDict = tool.readFromFile()
        # 注册菜单等功能
        self.api.listen_omega_menu(triggers=["gback"], argument_hint="", usage="返回公会中心", on_menu_invoked=self.menu_back)
        self.api.listen_omega_menu(triggers=["gcontribute"], argument_hint="", usage="消耗结晶碎片为公会增加贡献值", on_menu_invoked=self.menu_contribute)
        self.api.listen_omega_menu(triggers=["ginfo"], argument_hint="", usage="查询当前公会的信息", on_menu_invoked=self.menu_info)
        self.api.listen_omega_menu(triggers=["grank"], argument_hint="", usage="公会排名，且包含申请入会和OP管理功能", on_menu_invoked=self.menu_list)
        self.api.listen_omega_menu(triggers=["gmall"], argument_hint="", usage="§e[2级公会+]§b咕咕商城(Guild Edtion)", on_menu_invoked=self.menu_mall)
        self.api.listen_omega_menu(triggers=["gcreate"], argument_hint="", usage="§9[费用:结晶碎片*50w]§b在当前位置创建一个公会", on_menu_invoked=self.menu_create)
        self.api.listen_omega_menu(triggers=["gleave"], argument_hint="", usage="§b退出当前公会", on_menu_invoked=self.menu_leave)
        self.api.listen_omega_menu(triggers=["gupgrade"], argument_hint="", usage="§9[费用:公会贡献*50w]§e[§d高级会员§e+]§b升级公会，最高升级至4级", on_menu_invoked=self.menu_upgrade)
        self.api.listen_omega_menu(triggers=["gclose"], argument_hint="", usage="§e[§a公会管理§e+]§b设置公会禁入，开启后非公会会员无法进入公会区域", on_menu_invoked=self.menu_close)
        self.api.listen_omega_menu(triggers=["gmanage"], argument_hint="", usage="§e[§a公会管理§e+]§b人事管理，包含踢出会员和设置会员权限", on_menu_invoked=self.menu_manger)
        self.api.listen_omega_menu(triggers=["gverify"], argument_hint="", usage="§e[§a公会管理§e+]§b查看并审批入会申请", on_menu_invoked=self.menu_verify)
        self.api.listen_omega_menu(triggers=["gdissolution"], argument_hint="", usage="§e[§6公会会长§e]§b解散公会", on_menu_invoked=self.menu_dissolution)
        self.api.execute_in_individual_thread(self.protect)

omega.add_plugin(plugin=guildPlugin())
omega.run(addr=None)
