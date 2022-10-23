# 插件: 开
import random
from omega_side.python3_omega_sync import API
from omega_side.python3_omega_sync import frame as omega
from omega_side.python3_omega_sync.protocol import *
from API_By_Liliya import api

class autoAnswer:
    # 问答库
    QA = [
        {
            "questions":[
                "你好",
                "你们好",
                "大家好"
            ],
            "answers":[
                "你好啊！很高兴能遇见你！",
                "欢迎来到我们的服务器！"
            ]
        },
        {
            "questions":[
                "再见",
                "拜拜",
                "bye"
            ],
            "answers":[
                "欢迎下次再来哦~",
                "Bye~"
            ]
        },
        {
            "questions":[
                "怎么玩",
                "不会玩"
            ],
            "answers":[
                "可以在主城物资箱获取游玩指南哦！",
                "可以礼貌地向他人求助哦~"
            ]
        },
        {
            "questions":[
                "什么服务器"
            ],
            "answers":[
                "这是一个死亡掉落玩法的生存服~"
            ]
        },
        {
            "questions":[
                "怎么注册"
            ],
            "answers":[
                "现在无需注册即可游玩哦！请直接点击NPC前往主城吧！"
            ]
        },
        {
            "questions":[
                "兑换码"
            ],
            "answers":[
                "兑换码的获取请留意公告哦",
                "据说还有不少隐藏的兑换码哦，去问问其他玩家？",
                "请打开聊天栏菜单来使用兑换码吧！"
            ]
        },
        {
            "questions":[
                "打开菜单",
                "怎么用菜单",
                "菜单怎么用",
                "菜单怎么打开"
            ],
            "answers":[
                "在聊天栏发送加号(+)试试看？"
            ]
        },
        {
            "questions":[
                "怎么生存",
                "生存区"
            ],
            "answers":[
                "在主城点击“资源区大厅”NPC就能前往生存区哦"
            ]
        },
        {
            "questions":[
                "带我玩",
                "带带我",
                "求带",
                "救命"
            ],
            "answers":[
                "或许，你可以先试着自己努力下？",
                "我不能为你提供帮助哦"
            ]
        },
        {
            "questions":[
                "给我管理",
                "给我权限"
            ],
            "answers":[
                "服务器长期招收管理，可以加群了解哦！"
            ]
        },
        {
            "questions":[
                "给我东西",
                "送我东西"
            ],
            "answers":[
                "很遗憾我不能满足你的请求呢"
            ]
        },
        {
            "questions":[
                "有人吗",
                "有人在吗"
            ],
            "answers":[
                "你可以打开列表看看有没有其他玩家在线呢~",
                "我是机器人哦"
            ]
        },
        {
            "questions":[
                "你们在哪"
            ],
            "answers":[
                "不要随便将你的坐标告诉陌生人！"
            ]
        },
        {
            "questions":[
                "群号",
                "加群",
                "群聊"
            ],
            "answers":[
                "828234930，欢迎你的加入！"
            ]
        },
        {
            "questions":[
                "购买家园"
            ],
            "answers":[
                "购买家园请前往家园大厅哦"
            ]
        },
        {
            "questions":[
                "女装"
            ],
            "answers":[
                "啊这，很期待能看到你女装呢~"
            ]
        },
        {
            "questions":[
                "新手礼包",
                "萌新礼包",
                "新手物资"
            ],
            "answers":[
                "可以使用兑换码“新手物资”来获取礼包哦"
            ]
        },
        {
            "questions":[
                "死亡不掉落",
                "死亡掉落",
                "保留物品栏",
                "保留背包"
            ],
            "answers":[
                "死亡掉落是服务器的基本玩法哦",
                "这是一个死亡掉落的生存服~"
            ]
        },
        {
            "questions":[
                "LodenBot",
                "Lodenbot",
                "lodenbot"
            ],
            "answers":[
                "我是机器人哦，你可以打开聊天栏菜单获取我的帮助",
                "嗨嗨嗨，你好呀"
            ]
        },
    ]

    # 问题匹配模块
    def fuzzySearch(self, sentence):
        for item in self.QA:
            for question in item["questions"]:
                if question in sentence:
                    self.sendMsg(random.choice(item["answers"]))
                    return
        return

    # 游戏内消息发送模块
    def sendMsg(self, msg):
        self.api.send_all_player_msg(f"<LodenBot> {msg}")
        return

    # 游戏内消息监听模块
    def on_call(self, packet):
        if packet.TextType == 1:
            self.fuzzySearch(packet.Message)
        return

    def __call__(self, API:API):
        # 获取API
        self.api=api(API)
        # 注册消息监听
        self.api.listen_mc_packet(pkt_type="IDText", on_new_packet_cb=self.on_call)

omega.add_plugin(plugin=autoAnswer())
omega.run(addr=None)
