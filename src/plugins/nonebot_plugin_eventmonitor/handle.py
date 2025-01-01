"""事件处理"""

import httpx
import json
import nonebot

from typing import NoReturn
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import (
	Bot,
	Message,
	MessageSegment,
	PokeNotifyEvent,
	HonorNotifyEvent,
	GroupUploadNoticeEvent,
	GroupDecreaseNoticeEvent,
	GroupIncreaseNoticeEvent,
	GroupAdminNoticeEvent,
	LuckyKingNotifyEvent,
	GroupMessageEvent,
)

from .utils import utils
from .message import config

from .txt2img import txt_to_img


class Eventmonitor:
	@staticmethod
	async def chuo(
		matcher: Matcher, event: PokeNotifyEvent
	) -> None:
		"""戳一戳"""
		if not (
			await utils.check_chuo(
				utils.g_temp, str(event.group_id)
			)
		):
			await matcher.finish(utils.notAllow)
		# 获取用户id
		uid: str = event.get_user_id()
		try:
			cd = (
				event.time
				- utils.chuo_CD_dir[uid]
			)
		except KeyError:
			# 没有记录则cd为cd_time+1
			cd: int = utils.chuo_cd + 1
		if (
			cd > utils.chuo_cd
			or event.get_user_id()
			in nonebot.get_driver().config.superusers
		):
			utils.chuo_CD_dir.update(
				{uid: event.time}
			)
			rely_msg: str = (
				await config.chuo_send_msg()
			)
			if not (
				await utils.check_txt_to_img(
					utils.check_txt_img
				)
			):
				await matcher.finish(rely_msg)
			else:
				await matcher.send(
					MessageSegment.image(
						await txt_to_img.txt_to_img(
							rely_msg
						)
					)
				)

	@staticmethod
	async def qrongyu(
		matcher: Matcher,
		event: HonorNotifyEvent,
		bot: Bot,
	) -> None:
		"""群荣誉事件"""
		if not (
			await utils.check_honor(
				utils.g_temp, str(event.group_id)
			)
		):
			return
		bot_qq = int(bot.self_id)
		rely_msg: str = (
			await config.monitor_rongyu(
				event.honor_type,
				event.user_id,
				bot_qq,
			)
		)
		if not (
			await utils.check_txt_to_img(
				utils.check_txt_img
			)
		):
			await matcher.finish(rely_msg)
		else:
			await matcher.send(
				MessageSegment.image(
					await txt_to_img.txt_to_img(
						rely_msg
					)
				),
				at_sender=True,
			)

	@staticmethod
	async def files(
		matcher: Matcher,
		event: GroupUploadNoticeEvent,
	) -> None:
		"""群文件事件"""
		if not (
			await utils.check_file(
				utils.g_temp, str(event.group_id)
			)
		):
			return
		rely_msg = await config.upload_files(
			event.user_id
		)
		if not (
			await utils.check_txt_to_img(
				utils.check_txt_img
			)
		):
			await matcher.finish(rely_msg)
		else:
			await matcher.send(
				MessageSegment.image(
					await txt_to_img.txt_to_img(
						str(rely_msg)
					)
				),
				at_sender=True,
			)

	@staticmethod
	async def del_user(
		matcher: Matcher,
		event: GroupDecreaseNoticeEvent,
	) -> None:
		"""退群事件"""
		if not (
			await utils.check_del_user(
				utils.g_temp, str(event.group_id)
			)
		):
			return
		rely_msg = await config.del_user_bye(
			event.time, event.user_id
		)
		if not (
			await utils.check_txt_to_img(
				utils.check_txt_img
			)
		):
			await matcher.finish(rely_msg)
		else:
			await matcher.send(
				MessageSegment.image(
					await txt_to_img.txt_to_img(
						str(rely_msg)
					)
				),
				at_sender=True,
			)

	@staticmethod
	async def add_user(
		matcher: Matcher,
		event: GroupIncreaseNoticeEvent,
		bot: Bot,
	) -> None:
		"""入群事件"""
		await utils.config_check()
		if not (
			await utils.check_add_user(
				utils.g_temp, str(event.group_id)
			)
		):
			return
		bot_qq = int(bot.self_id)
		rely_msg = await config.add_user_wecome(
			event.time, event.user_id, bot_qq
		)
		if not (
			await utils.check_txt_to_img(
				utils.check_txt_img
			)
		):
			await matcher.finish(rely_msg)
		else:
			await matcher.send(
				MessageSegment.image(
					await txt_to_img.txt_to_img(
						str(rely_msg)
					)
				),
				at_sender=True,
			)

	@staticmethod
	async def admin_chance(
		matcher: Matcher,
		event: GroupAdminNoticeEvent,
		bot: Bot,
	) -> None:
		"""管理员变动事件"""
		if not (
			await utils.check_admin(
				utils.g_temp, str(event.group_id)
			)
		):
			return
		bot_qq = int(bot.self_id)
		rely_msg: str = (
			await config.admin_changer(
				event.sub_type,
				event.user_id,
				bot_qq,
			)
		)
		if not (
			await utils.check_txt_to_img(
				utils.check_txt_img
			)
		):
			await matcher.finish(rely_msg)
		else:
			await matcher.send(
				MessageSegment.image(
					await txt_to_img.txt_to_img(
						rely_msg
					)
				),
				at_sender=True,
			)

	@staticmethod
	async def hongbao(
		matcher: Matcher,
		event: LuckyKingNotifyEvent,
		bot: Bot,
	) -> None:
		"""红包运气王事件"""
		if not (
			await utils.check_red_package(
				utils.g_temp, str(event.group_id)
			)
		):
			return
		bot_qq = int(bot.self_id)
		rely_msg = (
			await config.rad_package_change(
				event.target_id, bot_qq
			)
		)
		if not (
			await utils.check_txt_to_img(
				utils.check_txt_img
			)
		):
			await matcher.finish(rely_msg)
		else:
			await matcher.send(
				MessageSegment.image(
					await txt_to_img.txt_to_img(
						rely_msg
					)
				),
				at_sender=True,
			)

	@staticmethod
	async def switch(
		matcher: Matcher, event: GroupMessageEvent
	) -> None:
		"""获取开关指令的参数，即用户输入的指令内容"""
		command = str(event.get_message()).strip()
		# 获取群组ID
		gid = str(event.group_id)
		# 判断指令是否包含"开启"或"关闭"关键字
		if '开启' in command or '开始' in command:
			if key := utils.get_command_type(
				command
			):
				utils.g_temp[gid][key] = True
				utils.write_group_data(
					utils.g_temp
				)
				name = utils.get_function_name(
					key
				)
				if not (
					await utils.check_txt_to_img(
						utils.check_txt_img
					)
				):
					await matcher.finish(
						f'{name}功能已开启喵'
					)
				else:
					await matcher.send(
						MessageSegment.image(
							await txt_to_img.txt_to_img(
								f'{name}功能已开启喵'
							)
						)
					)
		elif (
			'禁止' in command or '关闭' in command
		):
			if key := utils.get_command_type(
				command
			):
				utils.g_temp[gid][key] = False
				utils.write_group_data(
					utils.g_temp
				)
				name = utils.get_function_name(
					key
				)
				if not (
					await utils.check_txt_to_img(
						utils.check_txt_img
					)
				):
					await matcher.finish(
						f'{name}功能已关闭喵'
					)
				else:
					await matcher.send(
						MessageSegment.image(
							await txt_to_img.txt_to_img(
								f'{name}功能已关闭喵'
							)
						)
					)

	@staticmethod
	async def usage(matcher: Matcher) -> NoReturn:
		"""获取指令帮助"""
		await matcher.finish(utils.usage)

	@staticmethod
	async def state(
		matcher: Matcher, event: GroupMessageEvent
	) -> None:
		"""指令开关"""
		gid = str(event.group_id)
		with open(
			utils.address, 'r', encoding='utf-8'
		) as f:
			group_status = json.load(f)

		if gid not in group_status:
			await utils.config_check()
			with open(
				utils.address,
				'r',
				encoding='utf-8',
			) as f:
				group_status = json.load(f)

		rely_msg = (
			f'群{gid}的Event配置状态：\n'
			+ '\n'.join(
				[
					f"{utils.path[func][0]}: {'开启' if group_status[gid][func] else '关闭'}"
					for func in utils.path
				]
			)
		)
		if not (
			await utils.check_txt_to_img(
				utils.check_txt_img
			)
		):
			await matcher.finish(rely_msg)
		else:
			await matcher.send(
				MessageSegment.image(
					await txt_to_img.txt_to_img(
						rely_msg
					)
				)
			)

	@staticmethod
	async def check_bot(matcher: Matcher) -> None:
		"""检测插件更新"""
		try:
			if await eventmonitor.auto_check():
				await matcher.finish(
					'插件已是最新版本'
				)
		except Exception as e:
			logger.error(f'检查更新失败: {e}')
			await matcher.finish('检查更新失败')

	async def get_latest_version_data(
		self,
	) -> dict:
		for _ in range(3):
			try:
				async with (
					httpx.AsyncClient() as client
				):
					res = await client.get(
						f'https://ghgo.xyz{utils.release_url}'
					)
					if res.status_code == 200:
						return res.json()
			except TimeoutError:
				pass
			except Exception:
				logger.error('检查最新版本失败')
		return {}

	@staticmethod
	async def auto_check_bot_update() -> None:
		if utils.check_bot_update:
			await eventmonitor.auto_check()

	async def auto_check(self) -> None:
		bot = nonebot.get_bot()
		if utils.check_bot_update:
			data = await eventmonitor.get_latest_version_data()
			latest_version = data['name']
			if (
				utils.current_version
				!= latest_version
			):
				if (
					utils.current_version
					== latest_version
				):
					pass
				elif (
					utils.current_version
					< latest_version
				):
					await bot.send_private_msg(
						user_id=int(
							list(
								bot.config.superusers
							)[0]
						),
						message=Message(
							"✨插件自动检测更新✨\n"
							"插件名称: nonebot-plugin-eventmonitor\n"
							f"更新日期：{data['published_at']}\n"
							f"版本: {utils.current_version} -> {latest_version}\n"
							"主人可使用'检查event更新'指令自动更新插件"
						),
					)
				else:
					await bot.send_private_msg(
						user_id=int(
							list(
								bot.config.superusers
							)[0]
						),
						message=Message(
							f'获取到当前版本{utils.current_version} > {latest_version}\n'
							'请检查是否有报错并核查版本号'
						),
					)


eventmonitor = Eventmonitor()
