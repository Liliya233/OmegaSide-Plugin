# 插件: 开
import json
import time
from omega_side.python3_omega_sync import API
from omega_side.python3_omega_sync import frame as omega
from omega_side.python3_omega_sync.protocol import *
from API_By_Liliya import api

# 变量类
class param:
    dataFileName = '公会系统_By_Liliya'
    guildDict = {}
    powerNameList = ["§7普通会员§r", "§3高级会员§r", "§a公会管理§r", "§6公会会长§r"]

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
        return None

    # 通过UUID查询玩家公会权限
    def getPowerByUUID(UUID):
        playerObj = player.getByUUID(UUID)
        if playerObj:
            return player.getByUUID(UUID).power
        return None

    # 根据贡献值进行玩家排序
    def getSortedDict(members):
        return dict(sorted(members.items(), key=lambda x: x[1]['contribute'], reverse=True))

# 公会实体类
class guild:
    def __init__(self, name='', level=1, contribute=0, president='', isClosed=False, pos={'d':0, 'x':0, 'y':0, 'z':0}, members={}, applicants={}):
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
        # 申请列表
        self.applicants = applicants

    # 新增一个公会
    def add(guild):
        if guild.name not in param.guildDict:
            param.guildDict.update({guild.name: guild.__dict__})
            return True
        return False

    # 更新一个公会
    def update(guild):
        if guild.name in param.guildDict:
            param.guildDict.update({guild.name: guild.__dict__})
            return True
        return False

    # 删除一个公会
    def delete(guildName):
        if guildName in param.guildDict:
            param.guildDict.pop(guildName)
            return True
        return False

    # 通过公会昵称获取公会对象
    def getByName(guildName):
        if guildName in param.guildDict:
            guildObj = guild()
            guildObj.__dict__ = param.guildDict[guildName]
            return guildObj
        return None

    # 通过玩家UUID获取其归属的公会对象
    def getByUUID(UUID):
        for gkey in param.guildDict.keys():
            if UUID in param.guildDict[gkey]['members'].keys():
                return guild.getByName(gkey)
        return None

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
        return None
    
    # 根据权限列表获取指定公会的玩家列表
    def getMembersByPower(guildObj, powerList):
        result = []
        for data in guildObj.members.values():
            if data['power'] in powerList:
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

    # 通过坐标信息查询附件是否存在其他公会
    def hasGuildNearby(pos):
        for gdata in param.guildDict.values():
            # 判断
            if pos['d'] == gdata['pos']['d'] and (gdata['pos']['x']-900)<=pos['x']<=(gdata['pos']['x']+900) and (gdata['pos']['z']-900)<=pos['z']<=(gdata['pos']['z']+900):
                return True
        return False

    # 根据等级与贡献值进行公会排序
    def getSortedDict():
        return dict(sorted(param.guildDict.items(), key=lambda x: (x[1]['level'], x[1]['contribute']), reverse=True))

    # 获取申请列表
    def getApplicants(guildObj):
        result=[]
        for data in guildObj.applicants.values():
            result.append(data)
        return result

    # 查询玩家申请的公会
    def getApplying(UUID):
        for value in param.guildDict.values():
            for key in value["applicants"].keys():
                if key == UUID:
                    guildObj = guild()
                    guildObj.__dict__ = value
                    return guildObj
        return None

# 公会插件
class guildPlugin(object):
    def __init__(self, name:str="公会系统") -> None:
        self.name=name

    # 这三个函数需要调用api，包装一下放在这里吧
    def add_guild_and_save(self, guildObj):
        guild.add(guildObj)
        self.api.write_json_file(param.dataFileName, param.guildDict)

    def update_guild_and_save(self, guildObj):
        guild.update(guildObj)
        self.api.write_json_file(param.dataFileName, param.guildDict)

    def delete_guild_and_save(self, guildName):
        guild.delete(guildName)
        self.api.write_json_file(param.dataFileName, param.guildDict)

    # 菜单项-返回公会
    def menu_back(self, input:PlayerInput):
        playerName = input.Name
        UUID = self.api.get_player_uuid(playerName)
        # 获取公会
        guildObj = guild.getByUUID(UUID)
        # 是否拥有公会
        if not guildObj:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法使用此功能，你当前未加入任何公会哦！")
            return
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
        # 获取公会
        guildObj = guild.getByUUID(UUID)
        # 是否拥有公会
        if not guildObj:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法使用此功能，你当前未加入任何公会哦！")
            return
        # 判断是否扣费成功
        if not self.api.remove_player_score(playerName, 'money', count):
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c贡献失败！请确保你有足够的余额哦！")
            return
        # 增加贡献
        guildObj.contribute += count
        guildObj.members[UUID]['contribute'] += count
        # 存储写入
        self.update_guild_and_save(guildObj)
        self.api.do_send_player_msg(playerName, "§e[公会系统] §a感谢你为公会作出的贡献~")

    # 菜单项-公会信息
    def menu_info(self, input:PlayerInput):
        playerName = input.Name
        UUID = self.api.get_player_uuid(playerName)
        guildObj = guild.getByUUID(UUID)
        # 是否拥有公会
        if not guildObj:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法使用此功能，你当前未加入任何公会哦！")
            return
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
        for data in guild.getMembersByPower(guildObj, [1, 2, 3, 4]):
            rank+=1
            self.api.do_send_player_msg(playerName, f"§l§6{rank}.§r§e{data['name']} §b- {param.powerNameList[data['power'] - 1]} §b- §9贡献*{data['contribute']}")
        self.api.do_send_player_msg(playerName, "§l§aGUILD INFO - 显示完毕")

    # 菜单项-公会列表与功能
    def menu_list(self, input:PlayerInput):
        playerName = input.Name
        UUID = self.api.get_player_uuid(playerName)
        # 打印头部
        self.api.do_send_player_msg(playerName, "§l§aGUILD INFO - §b公会信息")
        # 打印列表
        guildNameList=[]
        for data in guild.getSortedDict().values():
            guildNameList.append(data['name'])
            self.api.do_send_player_msg(playerName, f"§l§6{len(guildNameList)} §r§b公会名：§e{data['name']} §b- 等级：§a{data['level']}级 §b- 当前贡献：§9{data['contribute']} §b- 会长：§6{data['members'][data['president']]['name']}")
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
            if guild.getByUUID(UUID):
                self.api.do_send_player_msg(playerName, "§e[公会系统] §c你已经加入一个公会啦！")
                return
            # 若处于申请状态，则撤销
            guildObj_1 = guild.getApplying(UUID)
            if guildObj_1:
                guildObj_1.applicants.pop(UUID)
                self.update_guild_and_save(guildObj_1)
            # 将玩家存入选中公会
            guildObj_2 = guild.getByName(guildNameList[select_1-1])
            guildObj_2.applicants.update({UUID: player(UUID=UUID, name=playerName).__dict__})
            self.update_guild_and_save(guildObj_2)
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
            for data in guild.getMembersByPower(guildObj, [1, 2, 3, 4]):
                rank+=1
                self.api.do_send_player_msg(playerName, f"§l§6{rank}.§r§e{data['name']} §b- {param.powerNameList[data['power'] - 1]} §b- §9贡献*{data['contribute']}")
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
                self.delete_guild_and_save(guildNameList[select_1-1])
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
        if guild.getByUUID(UUID):
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
        if not self.api.remove_player_score(playerName, 'money', 500000):
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c创建失败！请确保你有足够的余额哦！")
            return
        # 新建玩家对象
        playerObj = player(UUID=UUID, name=playerName, power=4)
        # 新建会员字典
        membersDict = {}
        membersDict.update({playerObj.UUID: playerObj.__dict__})
        # 新建公会对象
        guildObj = guild(name=guildName, pos=self.api.get_player_pos(playerName), members=membersDict, president=UUID)
        # 存储写入
        self.add_guild_and_save(guildObj)
        # 提示
        self.api.do_send_player_msg(playerName, "§e[公会系统] §a创建成功！快邀请其他小伙伴加入公会吧！")
        # 更新分数
        self.api.set_player_score(playerName, "guildLevel", 1)

    # 菜单项-公会商店
    def menu_mall(self, input:PlayerInput):
        # 获取玩家信息
        playerName = input.Name
        UUID = self.api.get_player_uuid(playerName)
        # 获取公会对象
        guildObj = guild.getByUUID(UUID)
        # 判断是否拥有公会
        if not guildObj or player.getPowerByUUID(UUID) < 2:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法使用此功能，只有2级或以上公会的会员才能使用哦！")
            return
        # 同步计分板
        self.api.set_player_score(playerName, "guildLevel", guildObj.level)
        if guildObj.level >= 2:
            self.api.do_send_wo_cmd(f"execute @a[name=\"{playerName}\"] ~~~ tell @a[tag=omg] +gmall-exec")
            self.api.do_send_wo_cmd(f"execute @a[name=\"{playerName}\"] ~~~ tell @a[tag=omg] 1")
            self.api.execute_after(func=lambda:self.api.do_send_player_msg(playerName, '§e[公会系统] §b请输入§e[物品序号] [购买数量]§b来进行批量购买吧~'), delay_time=1)

    # 菜单项-退出公会
    def menu_leave(self, input:PlayerInput):
        playerName = input.Name
        UUID = self.api.get_player_uuid(playerName)
        # 获取公会对象
        guildObj = guild.getByUUID(UUID)
        # 是否拥有公会
        if not guildObj:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法使用此功能，你当前未加入任何公会哦！")
            return
        # 是否会长
        if UUID == guildObj.president:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c会长不能退出公会哦！")
            return
        if self.api.do_get_get_player_next_param_input(playerName, hint="§e[公会系统] §b若要退出公会，请输入§e确认§b继续进行该操作(§d确认后不可撤销§b)：").input[0] == '确认':
            # 删除会员
            guildObj.members.pop(UUID)
            # 存储写入
            self.update_guild_and_save(guildObj)
            self.api.do_send_player_msg(playerName, "§e[公会系统] §a你已成功退出当前公会！")
            # 更新分数
            self.api.set_player_score(playerName, "guildLevel", 0)
        else:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c确认失败！本次操作已中断！")

    # 菜单项-公会帮助
    def menu_help(self, input:PlayerInput):
        playerName = input.Name
        self.api.do_send_player_msg(playerName, "§a简介：显示公会帮助指南，将在其他功能完成后进行编写")
        self.api.do_send_player_msg(playerName, "§e咕咕咕！打钱可以助力鸽子开发 (")

    # 管理菜单项-公会访客
    def menu_visit(self, input:PlayerInput):
        playerName = input.Name
        self.api.do_send_player_msg(playerName, "§a简介：高级会员+可以邀请非本公会的玩家进入公会区域，受邀请玩家将不受公会保护的约束，但无法享有公会增益效果。公会管理+可以禁用此项功能")
        self.api.do_send_player_msg(playerName, "§e咕咕咕！打钱可以助力鸽子开发 (")

    # 管理菜单项-公会营地
    def menu_camp(self, input:PlayerInput):
        playerName = input.Name
        self.api.do_send_player_msg(playerName, "§a简介：可以使用公会贡献购买主区域外的额外保护区域；可拥有营地的个数分别为：1， 2， 3；保护范围固定为200")
        self.api.do_send_player_msg(playerName, "§e咕咕咕！打钱可以助力鸽子开发 (")

    # 管理菜单项-公会增益
    def menu_gain(self, input:PlayerInput):
        playerName = input.Name
        self.api.do_send_player_msg(playerName, "§a简介：在公会区域内(包括营地)，为全体公会会员提供增益效果，公会访客不适用公会增益；可以使用公会贡献购买一定时长的增益效果")
        self.api.do_send_player_msg(playerName, "§e咕咕咕！打钱可以助力鸽子开发 (")

    # 管理菜单项-升级公会
    def menu_upgrade(self, input:PlayerInput):
        playerName = input.Name
        UUID = self.api.get_player_uuid(playerName)
        # 获取公会对象
        guildObj = guild.getByUUID(UUID)
        # 权限验证
        if not guildObj or player.getPowerByUUID(UUID) < 2:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法使用此功能，公会权限需要达到§3高级会员§c或以上")
            return
        # 等级上限
        if not guildObj.level < 4:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §a公会已达到最高等级，无需继续升级啦！")
            return
        # 尝试扣除贡献
        if guildObj.contribute < 500000:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c升级失败，公会贡献不足！")
            return
        guildObj.contribute -= 500000
        guildObj.level+=1
        # 存储写入
        self.update_guild_and_save(guildObj)
        self.api.do_send_player_msg(playerName, f"§e[公会系统] §a升级成功！当前公会等级为：§e{guildObj.level}级")
        # 更新分数
        for data in guildObj.members.values():
            self.api.set_player_score(data['name'], "guildLevel", guildObj.level)

    # 管理菜单项-公会禁入
    def menu_close(self, input:PlayerInput):
        playerName = input.Name
        UUID = self.api.get_player_uuid(playerName)
        # 获取公会对象
        guildObj = guild.getByUUID(UUID)
        # 权限验证
        if not guildObj or player.getPowerByUUID(UUID) < 3:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法使用此功能，公会权限需要达到§a公会管理§c或以上")
            return
        # 状态更新
        guildObj.isClosed = False if guildObj.isClosed else True
        # 存储写入
        self.update_guild_and_save(guildObj)
        self.api.do_send_player_msg(playerName, f"§e[公会系统] §a更改成功！当前公会禁入设置为：§e{'§c启用' if guildObj.isClosed else '§a禁用'}")

    # 管理菜单项-人员管理
    def menu_manger(self, input:PlayerInput):
        playerName = input.Name
        UUID = self.api.get_player_uuid(playerName)
        # 获取公会对象
        guildObj = guild.getByUUID(UUID)
        # 权限验证
        if not guildObj or player.getPowerByUUID(UUID) < 3:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法使用此功能，公会权限需要达到§a公会管理§c或以上")
            return
        # 列出会员
        self.api.do_send_player_msg(playerName, "§l§aGUILD MANAGE - §b会员管理")
        playerUUIDList=[]
        for data in guild.getMembersByPower(guildObj, [1, 2, 3, 4]):
            playerUUIDList.append(data['UUID'])
            self.api.do_send_player_msg(playerName, f"§l§6{len(playerUUIDList)}.§r§e{data['name']} §b- {param.powerNameList[data['power'] - 1]} §b- §9贡献*{data['contribute']}")
        self.api.do_send_player_msg(playerName, "§l§aGUILD MANAGE - §d请根据下方提示进行输入")
        # 获取玩家选择
        try:
            select_1 = int(self.api.do_get_get_player_next_param_input(playerName, hint="§e[公会系统] §b请输入一个玩家编号，进行下一步操作：").input[0]) - 1
        except Exception:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c只能输入编号哦！")
            return
        # 判断是否越界
        if not 0 <= select_1 < len(playerUUIDList):
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c不存在这个选项哦！")
            return
        # 打印头部
        self.api.do_send_player_msg(playerName, "§l§aGUILD MANAGE - §b会员管理")
        self.api.do_send_player_msg(playerName, f"§7当前已选中会员：§e{player.getByUUID(playerUUIDList[select_1]).name}")
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
            if player.getPowerByUUID(UUID) < 3:
                self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法使用此功能，公会权限需要达到§a公会管理§c或以上")
                return
            # 权限对比
            elif player.getPowerByUUID(UUID) == 3 and player.getPowerByUUID(playerUUIDList[select_1]) > 2:
                self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法移除，当前权限等级仅允许移除§7普通会员§c与§3高级会员")
                return
            elif player.getPowerByUUID(playerUUIDList[select_1]) == 4:
                self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法移除，当前权限等级仅允许移除§7普通会员§c、§3高级会员§c与§a公会管理")
                return
            # 更新分数
            self.api.set_player_score(player.getByUUID(playerUUIDList[select_1]).name, "guildLevel", 0)
            # 移除会员
            guildObj.members.pop(playerUUIDList[select_1])
            # 存储写入
            self.update_guild_and_save(guildObj)
            self.api.do_send_player_msg(playerName, "§e[公会系统] §a已成功将该会员移出公会！")
        elif select_2 in ['2', 'setpower']:
            # 权限验证
            if player.getPowerByUUID(UUID) < 4:
                self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法使用此功能，公会权限需要达到§6公会会长")
                return
            # 权限对比
            if player.getPowerByUUID(playerUUIDList[select_1]) == 4:
                self.api.do_send_player_msg(playerName, "§e[公会系统] §c会长权限不允许更改哦！")
                return
            # 打印头部
            self.api.do_send_player_msg(playerName, "§l§aGUILD MANAGE - §b会员管理")
            self.api.do_send_player_msg(playerName, f"§7当前已选中会员：§e{player.getByUUID(playerUUIDList[select_1]).name}")
            # 打印选项列表
            self.api.do_send_player_msg(playerName, "§l§61 §eordinary §r§b将该名会员的权限设置为§7普通会员")
            self.api.do_send_player_msg(playerName, "§l§62 §esenior §r§b将该名会员的权限设置为§3高级会员")
            self.api.do_send_player_msg(playerName, "§l§63 §emanagement §r§b将该名会员的权限设置为§a公会管理")
            # 打印尾部
            self.api.do_send_player_msg(playerName, "§l§aGUILD MANAGE - §d请根据下方提示进行输入")
            # 获取玩家选择
            select_3 = self.api.do_get_get_player_next_param_input(playerName, hint="§e[公会系统] §b请输入要设置的权限：").input[0]
            pl = player.getByUUID(playerUUIDList[select_1])
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
            self.update_guild_and_save(guildObj)
            self.api.do_send_player_msg(playerName, "§e[公会系统] §a已成功更改该名会员的权限！")
        else:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c不存在这个选项哦！")

    # 管理菜单项-人员审批
    def menu_verify(self, input:PlayerInput):
        playerName = input.Name
        UUID = self.api.get_player_uuid(playerName)
        # 获取公会对象
        guildObj = guild.getByUUID(UUID)
        # 权限验证
        if not guildObj or player.getPowerByUUID(UUID) < 3:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法使用此功能，公会权限需要达到§a公会管理§c或以上")
            return
        # 列出待审核会员
        self.api.do_send_player_msg(playerName, "§l§aGUILD VERIFY - §b会员审批")
        playerList=[]
        for data in guild.getApplicants(guildObj):
            playerList.append(data)
            self.api.do_send_player_msg(playerName, f"§l§6{len(playerList)}.§r§e{data['name']} §b- §c等待审批")
        self.api.do_send_player_msg(playerName, "§l§aGUILD VERIFY - §d请根据下方提示进行输入")
        # 获取玩家选择
        try:
            select_1 = int(self.api.do_get_get_player_next_param_input(playerName, hint="§e[公会系统] §b请输入一个玩家编号，进行下一步操作：").input[0]) - 1
        except Exception:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c只能输入编号哦！")
            return
        # 判断是否越界
        if not 0 <= select_1 < len(playerList):
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c不存在这个选项哦！")
            return
        # 选中的玩家
        selected_pl = playerList[select_1]
        # 打印头部
        self.api.do_send_player_msg(playerName, "§l§aGUILD VERIFY - §b会员审批")
        self.api.do_send_player_msg(playerName, f"§7当前已选中玩家：§e{selected_pl['name']}")
        # 打印选项列表
        self.api.do_send_player_msg(playerName, "§l§61 §eallow §r§b同意该入会申请")
        self.api.do_send_player_msg(playerName, "§l§62 §edeny §r§b拒绝该入会申请")
        # 打印尾部
        self.api.do_send_player_msg(playerName, "§l§aGUILD VERIFY - §d请根据下方提示进行输入")
        # 获取玩家选择
        select_2 = self.api.do_get_get_player_next_param_input(playerName, hint="§e[公会系统] §b请输入一个选项编号，进行下一步操作：").input[0]
        # 功能项
        if select_2 in ['1', 'allow']:
            selected_pl['power'] = 1
            guildObj.members.update({selected_pl['UUID']: selected_pl})
            guildObj.applicants.pop(selected_pl['UUID'])
            self.api.do_send_player_msg(playerName, "§e[公会系统] §a你同意了该入会申请！")
            # 更新分数
            self.api.set_player_score(selected_pl['name'], "guildLevel", guildObj.level)
        elif select_2 in ['2', 'deny']:
            guildObj.applicants.pop(selected_pl['UUID'])
            self.api.do_send_player_msg(playerName, "§e[公会系统] §a你拒绝了该入会申请！")
        else:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c不存在这个选项哦！")
            return
        # 存储写入
        self.update_guild_and_save(guildObj)

    # 管理菜单项-公会解散
    def menu_dissolution(self, input:PlayerInput):
        playerName = input.Name
        UUID = self.api.get_player_uuid(playerName)
        # 获取公会对象
        guildObj = guild.getByUUID(UUID)
        # 权限验证
        if not guildObj or player.getPowerByUUID(UUID) < 4:
            self.api.do_send_player_msg(playerName, "§e[公会系统] §c无法使用此功能，公会权限需要达到§6公会会长")
            return
        # 再次确认
        if self.api.do_get_get_player_next_param_input(playerName, hint="§e[公会系统] §b若要解散公会，请输入§e立即解散§b继续进行该操作(§d确认后不可撤销§b)：").input[0] == '立即解散':
            # 更新分数
            for data in guildObj.members.values():
                self.api.set_player_score(player.getByUUID(data['name']), "guildLevel", 0)
            # 解散公会
            self.delete_guild_and_save(guildObj.name)
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
                    playerPos = self.api.get_player_pos(playerName)
                    # 尝试获取公会
                    guildObj_1 = guild.getByPos(playerPos)
                    guildObj_2 = guild.getByUUID(playerUUID)
                    # 判断
                    if guildObj_1:
                        # 通用
                        self.api.do_send_wo_cmd(f"title @a[name=\"{playerName}\",scores={{menu=0}}] actionbar §b当前位于公会区域 - §e{guildObj_1.name}")
                        self.api.do_send_wo_cmd(f"tag @a[name=\"{playerName}\"] add 公会区域")
                        # 是否为所属公会
                        if guildObj_1 is guildObj_2:
                            # 如果玩家改名，此时会被更新
                            if guildObj_1.members[playerUUID]['name'] is not playerName:
                                guildObj_1.members[playerUUID]['name'] = playerName
                                self.update_guild_and_save(guildObj_1)
                        else:
                            if guildObj_1.isClosed:
                                board = guild.getBoard(guildObj_1, playerPos)
                                self.api.do_send_wo_cmd(f"tp @a[name=\"{playerName}\",m=!c] {board['x']} {board['y']} {board['z']}")
                                self.api.do_send_wo_cmd(f"titleraw @a[name=\"{playerName}\",m=!c] actionbar {{\"rawtext\":[{{\"text\":\"§c当前公会不允许非公会成员进入\"}}]}}")
                            else:
                                self.api.do_send_wo_cmd(f"gamemode a @a[name=\"{playerName}\",m=s]")
                    else:
                        self.api.do_send_wo_cmd(f"title @a[name=\"{playerName}\",scores={{menu=0}},tag=公会区域] actionbar §b已离开公会区域")
                        self.api.do_send_wo_cmd(f"tag @a[name=\"{playerName}\",tag=公会区域] remove 公会区域")
            except Exception:
                pass

    def __call__(self, API:API):
        # 获取API
        self.api=api(API)
        # 读取公会信息
        param.guildDict = self.api.read_json_file(param.dataFileName)
        # 注册菜单等功能
        self.api.listen_omega_menu(triggers=["gback"], argument_hint="", usage="返回公会中心", on_menu_invoked=self.menu_back)
        self.api.listen_omega_menu(triggers=["gcontribute"], argument_hint="", usage="消耗结晶碎片为公会增加贡献值", on_menu_invoked=self.menu_contribute)
        self.api.listen_omega_menu(triggers=["ginfo"], argument_hint="", usage="查询当前公会的信息", on_menu_invoked=self.menu_info)
        self.api.listen_omega_menu(triggers=["grank"], argument_hint="", usage="公会排名，且包含申请入会和OP管理功能", on_menu_invoked=self.menu_list)
        self.api.listen_omega_menu(triggers=["gmall"], argument_hint="", usage="§e[2级公会+]§b咕咕商城(Guild Edtion)", on_menu_invoked=self.menu_mall)
        self.api.listen_omega_menu(triggers=["gcreate"], argument_hint="", usage="§9[费用:结晶碎片*50w]§b在当前位置创建一个公会", on_menu_invoked=self.menu_create)
        self.api.listen_omega_menu(triggers=["gleave"], argument_hint="", usage="退出当前公会", on_menu_invoked=self.menu_leave)
        self.api.listen_omega_menu(triggers=["ghelp"], argument_hint="", usage="获取公会相关帮助", on_menu_invoked=self.menu_help)
        self.api.listen_omega_menu(triggers=["gvisit"], argument_hint="", usage="§e[§3高级会员§e+]§b设置与授权公会访客访问权限", on_menu_invoked=self.menu_visit)
        self.api.listen_omega_menu(triggers=["gcamp"], argument_hint="", usage="§e[2级公会+][§a公会管理§e+]§b购买与设置公会营地", on_menu_invoked=self.menu_camp)
        self.api.listen_omega_menu(triggers=["ggain"], argument_hint="", usage="§e[2级公会+][§a公会管理§e+]§b购买公会增益时长", on_menu_invoked=self.menu_gain)
        self.api.listen_omega_menu(triggers=["gupgrade"], argument_hint="", usage="§9[费用:公会贡献*50w]§e[§3高级会员§e+]§b升级公会，最高升级至4级", on_menu_invoked=self.menu_upgrade)
        self.api.listen_omega_menu(triggers=["gclose"], argument_hint="", usage="§e[§a公会管理§e+]§b设置公会禁入，开启后非公会会员无法进入公会区域", on_menu_invoked=self.menu_close)
        self.api.listen_omega_menu(triggers=["gmanage"], argument_hint="", usage="§e[§a公会管理§e+]§b人事管理，包含踢出会员和设置会员权限", on_menu_invoked=self.menu_manger)
        self.api.listen_omega_menu(triggers=["gverify"], argument_hint="", usage="§e[§a公会管理§e+]§b查看并审批入会申请", on_menu_invoked=self.menu_verify)
        self.api.listen_omega_menu(triggers=["gdissolution"], argument_hint="", usage="§e[§6公会会长§e]§b解散公会", on_menu_invoked=self.menu_dissolution)
        self.api.execute_in_individual_thread(self.protect)

omega.add_plugin(plugin=guildPlugin())
omega.run(addr=None)
