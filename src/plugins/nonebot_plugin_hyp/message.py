"""构造回复消息"""


class Message:
	@staticmethod
	async def send_hyp_msg(
		data, data_a, online
	) -> str:
		"""构建/hyp回复消息"""
		error = data.get('e')
		if error:
			return error
		else:
			msg = (
				f"{data['rank']} {data_a['displayname']} 的Hypixel信息:\n"
				f"等级: {data['level']} | 人品: {data['karma']}\n"
				f"在线情况: {online} | 成就点数: {data['achievementPoints']}\n"
				f"完成任务: {data['quest_master']} | 完成挑战: {data['challenger']}\n"
				f"小游戏胜场: {data['general_wins']} | 获得硬币: {data['general_coins']}\n"
				f"活动银币: {data['silver']} | 战魂: {data['total_tributes']}\n"
				f"使用语言: {data['language']}\n"
				f"首次登陆: {data['first_login']}\n"
				f"上次登录: {data['last_login']}\n"
				f"上次退出: {data['lastLogout']}\n"
				f"最近游玩: {data['recentgame']}"
			)
			return msg

	@staticmethod
	async def send_apikey_msg(
		hyp_apikey, ant_apikey
	):
		msg = (
			f'当前API信息如下:\n'
			f'hypixel-apikey: {hyp_apikey}\n'
			f'- - - - - - - - - - - - - - - - - - - - - - '
			'- - - - - - - - - - - - - - - - - - - - - - - \n'
			f'antisniper-apikey: {ant_apikey}'
		)
		return msg

	@staticmethod
	async def send_mc_msg(data):
		"""构建/mc回复消息"""
		error = data.get('e')
		if error:
			return error
		else:
			msg = (
				f"ID: {data['name']}\n"
				f"UUID: {data['id']}"
			)
			return msg

	@staticmethod
	async def send_bw_msg(
		data, data_a, rank
	) -> str:
		"""构建/bw回复消息"""
		error = data.get('e')
		if error:
			return error
		else:
			msg = (
				f"[{data['bw_level']}] {rank} {data_a['displayname']} 的起床战争数据:\n"
				f"经验: {data['bw_experience']} | 硬币: {data['bw_coin']} | 连胜: {data['winstreak']}\n"
				f"拆床: {data['break_bed']} | 被拆床: {data['lost_bed']} | BBLR: {data['BBLR']}\n"
				f"胜场: {data['bw_win']} | 败场: {data['bw_losses']} | W/L: {data['W_L']}\n"
				f"击杀: {data['bw_kill']} | 死亡: {data['bw_death']} | K/D: {data['K_D']}\n"
				f"终杀: {data['bw_final_kill']} | 终死: {data['bw_final_death']} | FKDR: {data['FKDR']}\n"
				f"收集铁锭: {data['bw_iron']} | 收集金锭: {data['bw_gold']}\n"
				f"收集钻石: {data['bw_diamond']} | 收集绿宝石: {data['bw_emerald']}\n"
			)
			return msg

	@staticmethod
	async def send_sw_msg(
		data, data_a, rank
	) -> str:
		"""构建/sw回复消息"""
		error = data.get('e')
		if error:
			return error
		else:
			msg = (
				f"[{data['sw_level']}] {rank} {data_a['displayname']}的空岛战争数据：\n"
				f"经验: {data['sw_experience']} | 硬币:{data['sw_coins']} | 代币:{data['sw_cosmetic_tokens']}\n"
				f"胜场: {data['sw_wins']} | 败场: {data['sw_losses']} | W/L: {data['SW_W_L']}\n"
				f"击杀: {data['sw_kills']} | 死亡: {data['sw_deaths']} | K/D: {data['SW_K_D']}\n"
				f"总场次:{data['sw_games']} | 连胜: {data['sw_win_streak']} | 助攻: {data['sw_assists']}\n"
				f"灵魂: {data['sw_souls']} | 最短胜利时间: {data['sw_fastest_win']}s\n"
				f"上次游玩: {data['sw_lastMode']} | 游戏时长: {data['sw_time_played']}"
			)
			return msg


msg = Message()
