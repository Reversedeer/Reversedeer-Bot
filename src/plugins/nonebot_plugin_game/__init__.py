"""插件入口"""
import contextlib
import nonebot
import os

from nonebot import on_command

from .handle import game
from . utils import utils
from .database import DATA_PATH
on_command(
    "签到",
    priority=20,
    block=True,
    handlers=[game.sign]

)

on_command(
    "钓鱼",
    priority=20,
    block=False,
    handlers=[game.fish]
    
)
driver = nonebot.get_driver()
@driver.on_bot_connect
async def _():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)

with contextlib.suppress(Exception):
    from nonebot.plugin import PluginMetadata

    __plugin_meta__ = PluginMetadata(
        name="dog",
        description="随机返回一句舔狗日记...嘤嘤嘤和其他文案的插件",
        usage=utils.usage,
        type="application",
        homepage="https://github.com/Reversedeer/nonebot_plugin_game",
        supported_adapters={"onebot.v11"},
        extra={
            "author": "Reversedeer",
            "version": "0.0.1",
            "priority": 20,
        },
    )