from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment, ActionFailed
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.exception import FinishedException
from nonebot.internal.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from pyppeteer import launch

from .path import *
from .utils import json_load, json_upload, fi, log_fi

switcher = on_command(
    '开启',
    aliases={"关闭"},
    priority=15,
    block=True,
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER
    )


@switcher.handle()
async def _(matcher: Matcher, event: GroupMessageEvent):
    gid = str(event.group_id)
    funcs_status = json_load(switcher_path)
    command = str(event.get_message()).strip()
    if "开启" in command or "开始" in command:
        if key := get_command_type(command):
            funcs_status[gid][key] = True
            json_upload(switcher_path, funcs_status)
            name = get_function_name(key)
            await matcher.finish(f"{name}功能已开启喵")
    
    elif "关闭" in command or "禁止" in command:
        if key := get_command_type(command):
            funcs_status[gid][key] = False
            json_upload(switcher_path, funcs_status)
            name = get_function_name(key)
            await matcher.finish(f"{name}功能已禁用喵")
            
#根据关键词获取对应功能名称
def get_function_name(key: str) -> str:
    return admin_funcs[key][0]

#根据指令内容获取开关类型
def get_command_type(command: str) -> str:
    return next(
        (
            key
            for key, keywords in admin_funcs.items()
            if any(keyword in command for keyword in keywords)
        ),
        "",
    )

switcher_html = on_command(
    '群管状态',
    aliases={"admin状态"},
    priority=15,
    block=True,
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER
    )


@switcher_html.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    gid = str(event.group_id)
    funcs_status = json_load(switcher_path)
    try:
        await log_fi(matcher,
                     '当前群组开关状态：\n' + '\n'.join(
                         [f"{admin_funcs[func][0]}：{'开启' if funcs_status[gid][func] else '关闭'}" for func in
                          admin_funcs]))
    except ActionFailed:
        await log_fi(matcher,
                     '当前群组开关状态：\n' + '\n'.join(
                         [f"{admin_funcs[func][0]}：{'开启' if funcs_status[gid][func] else '关闭'}" for func in
                          admin_funcs]),
                     '可能被风控，已使用文字发送', err=True)
    except FinishedException:
        pass
    except Exception as e:
        await log_fi(matcher,
                     '当前群组开关状态：\n' + '\n'.join(
                         [f"{admin_funcs[func][0]}：{'开启' if funcs_status[gid][func] else '关闭'}" for func in
                          admin_funcs]),
                     f'开关渲染网页并截图失败，已使用文字发送，错误信息：\n{"-" * 30}{type(e)}: {e}{"-" * 30}', err=True)


async def save_image(url, img_path):
    """
    导出图片
    :param url: 在线网页的url
    :param img_path: 图片存放位置
    :return:
    """
    browser = await launch(options={'args': ['--no-sandbox']}, handleSIGINT=False)
    page = await browser.newPage()
    # 加载指定的网页url
    await page.goto(url)
    # 设置网页显示尺寸
    await page.setViewport({'width': 1920, 'height': 1080})
    """
    path: 图片存放位置
    clip: 位置与图片尺寸信息
        x: 网页截图的x坐标
        y: 网页截图的y坐标
        width: 图片宽度
        height: 图片高度
    """
    await page.screenshot({'path': img_path, 'clip': {'x': 0, 'y': 0, 'width': 320, 'height': 800}})
    await browser.close()


async def switcher_integrity_check(bot: Bot):
    g_list = (await bot.get_group_list())
    switcher_dict = json_load(switcher_path)
    for group in g_list:
        gid = str(group['group_id'])
        if not switcher_dict.get(gid):
            switcher_dict[gid] = {}
            for func in admin_funcs:
                if func in ['img_check', 'auto_ban', 'group_msg', 'particular_e_notice', 'group_recall']:
                    switcher_dict[gid][func] = False
                else:
                    switcher_dict[gid][func] = True
        else:
            this_group_switcher = switcher_dict[gid]
            for func in admin_funcs:
                if this_group_switcher.get(func) is None:
                    if func in ['img_check', 'auto_ban', 'group_msg', 'particular_e_notice', 'group_recall']:
                        this_group_switcher[func] = False
                    else:
                        this_group_switcher[func] = True
    json_upload(switcher_path, switcher_dict)


