from nonebot import on_command

from . import server_status, status_config, status_permission

if status_config.server_status_enabled:
    command = on_command(
        "status",
        aliases={"机器状态"},
        permission=status_permission,
        priority=2,
        handlers=[server_status],
    )
