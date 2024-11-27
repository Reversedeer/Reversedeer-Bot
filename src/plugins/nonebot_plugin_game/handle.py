"""handle模块"""

from nonebot.adapters.onebot.v11 import (
	GroupMessageEvent,
	MessageSegment,
	Message,
)
from nonebot.matcher import Matcher
from nonebot.log import logger
from datetime import date, timedelta
import random

from .database import (
	check_group_allow,
	is_in_table,
	get_today,
	insert_sign,
)

from .utils import utils


class Game:
	@staticmethod
	async def fish() -> None:
		pass

	@staticmethod
	async def sign(
		matcher: Matcher, event: GroupMessageEvent
	) -> None:
		"""签到响应器"""
		if not check_group_allow(event.group_id):
			await matcher.finish(
				utils.not_allow, at_sender=True
			)
		uid: str = event.get_user_id()
		if is_in_table(userid=int(uid)):
			pass

	async def get_integral(self) -> None:
		integral_num = random.randint(50, 150)
		insert_sign(int())


game = Game()
