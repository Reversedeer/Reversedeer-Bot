"""主要函数"""

import asyncio

from nonebot.adapters.onebot.v11 import Message
from nonebot import get_plugin_config
from nonebot.params import CommandArg
from typing import Callable, NoReturn
from nonebot.matcher import Matcher

from .utils import Config
from .message import msg
from .api import api

plugin_config = get_plugin_config(Config)


class Hyp:
	async def hyp(
		self,
		matcher: Matcher,
		arg: Message = CommandArg(),
	) -> NoReturn:
		"""hypixel"""
		args: list[str] = str(arg).strip().split()
		if len(args) < 1:
			await matcher.finish(
				'请提供一个有效的ID'
			)
		uid: str = args[0]

		if len(args) == 1:
			# 当只有一个 id参数时
			players_data: dict = (
				await api.player_data(uid)
			)
			data_a: str = players_data[
				'player_data'
			]
			data_b: str = players_data[
				'player_status'
			]
			tasks: list = [
				api.get_hypixel_data(data_a),
				api.get_player_online(data_b),
			]
			(
				data,
				online,
			) = await asyncio.gather(*tasks)
			reply: str = await msg.send_hyp_msg(
				data, data_a, online
			)
			await matcher.finish(reply)

		elif len(args) == 2:
			# 如果有第二个参数，则动态调用函数
			action: str = args[1]
			actions: dict[
				str, Callable[[Matcher, Message]]
			] = {
				'bw': hyp.bw,
				'sw': hyp.sw,
				'mc': hyp.mc,
			}
			if action not in actions:
				await matcher.finish(
					f"未知指令：'{action},'支持的操作有：{', '.join(actions.keys())}"
				)
			await actions[action](
				matcher, Message(uid)
			)

	async def hypapi(
		self, matcher: Matcher
	) -> NoReturn:
		hyp_apikey: str = (
			plugin_config.hypixel_apikey
		)
		ant_apikey: str = (
			plugin_config.antisniper_apikey
		)
		reply: str = await msg.send_apikey_msg(
			hyp_apikey, ant_apikey
		)
		await matcher.finish(reply)

	async def mc(
		self,
		matcher: Matcher,
		arg: Message = CommandArg(),
	) -> NoReturn:
		"""minecraft"""
		args: list[str] = str(arg).strip().split()
		if len(args) < 1:
			await matcher.finish(
				'请提供一个有效的ID'
			)
		uid: str = args[0]
		data: dict = await api.get_mc_data(uid)
		reply: str = await msg.send_mc_msg(data)
		await matcher.finish(reply)

	async def bw(
		self,
		matcher: Matcher,
		arg: Message = CommandArg(),
	) -> NoReturn:
		"""bedwars"""
		args: list[str] = str(arg).strip().split()
		if len(args) < 1:
			await matcher.finish(
				'请提供一个有效的ID'
			)
		uid: str = args[0]
		players_data: dict = (
			await api.player_data(uid)
		)
		data_a: str = players_data['player_data']
		tasks: list = [
			api.get_players_bedwars(data_a),
			api.get_player_rack(data_a),
		]
		(
			data,
			rank,
		) = await asyncio.gather(*tasks)
		reply: str = await msg.send_bw_msg(
			data, data_a, rank
		)
		await matcher.finish(reply)

	async def sw(
		self,
		matcher: Matcher,
		arg: Message = CommandArg(),
	) -> NoReturn:
		"""skywars"""
		args: list[str] = str(arg).strip().split()
		if len(args) < 1:
			await matcher.finish(
				'请提供一个有效的ID'
			)
		uid: str = args[0]
		players_data: dict = (
			await api.player_data(uid)
		)
		data_a: str = players_data['player_data']
		tasks: list = [
			api.get_players_skywars(data_a),
			api.get_player_rack(data_a),
		]
		(
			data,
			rank,
		) = await asyncio.gather(*tasks)
		reply: str = await msg.send_sw_msg(
			data, data_a, rank
		)
		await matcher.finish(reply)


hyp = Hyp()
