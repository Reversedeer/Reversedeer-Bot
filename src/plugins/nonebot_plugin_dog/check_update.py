import os
import httpx
from nonebot import on_command
from .utils import current_version
from nonebot.permission import SUPERUSER
from __init__ import check, restart


@check.handle()
async def check_update():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://pypi.org/pypi/nonebot-plugin-dog/json')
        data = response.json()
        latest_version = data['info']['version']
        if current_version != latest_version:
            await check.finish((f'=======插件更新=======\nnonebot-plugin-dog\n当前Version: {current_version}\n最新Version: {latest_version}\n======插件可更新======'), block = False)
        else:
            await check.finish((f'=======插件更新=======\nnonebot-plugin-dog\n当前Version：{latest_version}\n======插件已最新======'), block=False)

@restart.got("flag", prompt="确定是否重启？确定请回复[是|好|确定]（重启失败咱们将失去联系，请谨慎！）")
async def _(flag: str = ArgStr("flag")):
    if flag.lower() in ["true", "是", "好", "确定", "确定是"]:
        await restart.send("开始重启..请稍等...")
        open("new_version", "w")
        os.system("./restart.sh")
    else:
        await restart.send("已取消操作...")
        