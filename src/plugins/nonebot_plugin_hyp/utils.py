"""依赖文件"""

import nonebot


class Utils:
	def __init__(self) -> None:
		self.usage = """
		    指令1: help 显示指令列表
			指令2:mc|minecraft|profile|skin|mcskin <玩家> 查询玩家 Minecraft 信息
			指令3:mcuuid|uuid <UUID> 查询 UUID 玩家信息
			指令4:hyp|hypixel <玩家> [游戏] 查询 Hypixel 信息
			指令5:hypapi 查询当前使用的 API Key 信息
			指令6:ban|bans|punishment|punishments 查询封禁信息
			指令7:bw|bedwar|bedwars <玩家> [模式] 查询起床战争数据
			指令8:sw|skywar|skywars <玩家> 查询空岛战争数据
			指令9:mw|megawall|megawalls <玩家> 查询超级战墙数据
			指令10:duel|duels <玩家> [模式] 查询决斗游戏数据
			指令11:bsg|blitz <玩家> 查询闪电饥饿游戏数据
			指令12:uhc <玩家> 查询 UHC 数据
			指令13:mm|murder <玩家> 查询密室杀手数据
			指令14:tnt|tntgame|tntgames <玩家> 查询掘战游戏数据
			指令15:pit <玩家> 查询天坑之战数据
			指令16:gname|guildname <公会名称> 查询公会
			指令17:g|guild <玩家> 查询玩家所在公会
			指令18:bwshop|bwfav <玩家> 查询玩家起床战争商店
			指令19:denick <Nick> 查询 Nick (Antisniper)
			指令20:findnick <玩家> 查找 Nick (Antisniper)
			指令21:ws|winstreak <玩家> 查询起床战争普通模式连胜 (Antisniper)
			指令22:wsall|winstreakall <玩家> 查询起床战争其他模式连胜 (Antisniper)
			指令23:wshyp <玩家> 查询起床战争普通模式连胜 (Hypixel)
			指令24:wsallhyp <玩家> 查询起床战争其他模式连胜 (Hypixel)
			指令25:of|optifine <玩家> 查询 OptiFine 披风
		"""
		driver = nonebot.get_driver().config
		self.hypixel_apikey: int = getattr(
			driver,
			'hypixel_apikey',
			1145141919810,
		)
		self.antisniper_apikey: int = getattr(
			driver,
			'antisniper_apikey',
			1145141919810,
		)


utils = Utils()
