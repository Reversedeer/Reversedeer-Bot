from nonebot.rule import to_me
from nonebot import on_type, on_message
from nonebot.adapters.onebot.v11 import PokeNotifyEvent, PrivateMessageEvent

from . import server_status, status_config, status_permission

if status_config.server_status_enabled:
    group_poke = on_type(
        (PokeNotifyEvent,),
        rule=to_me(),
        permission=status_permission,
        priority=2,
        block=True,
        handlers=[server_status],
    )


async def _poke(event: PrivateMessageEvent) -> bool:
    return event.sub_type == "friend" and event.message[0].type == "poke"


if status_config.server_status_enabled:
    poke = on_message(
        _poke,
        permission=status_permission,
        priority=2,
        block=True,
        handlers=[server_status],
    )
