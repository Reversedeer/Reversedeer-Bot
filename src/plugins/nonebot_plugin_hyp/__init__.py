"""入口文件"""

from nonebot.plugin import PluginMetadata, on_command

from .utils import Config, utils
from .handle import hyp

# from nonebot import require
# require('nonebot_plugin_localstore')

on_command(
    'hyp',
    aliases={'hypixel'},
    priority=10,
    block=False,
    handlers=[hyp.hyp],
)

on_command(
    'hypapi',
    priority=10,
    block=False,
    handlers=[hyp.hypapi],
)
on_command(
    'mc',
    aliases={'minecraft'},
    priority=10,
    block=False,
    handlers=[hyp.mc],
)

on_command(
    'bw',
    aliases={'bedwars'},
    priority=10,
    block=False,
    handlers=[hyp.bw],
)

on_command(
    'sw',
    aliases={'skywars'},
    priority=10,
    block=False,
    handlers=[hyp.sw],
)

__plugin_meta__ = PluginMetadata(
    name='nonebot-plugin-hyp',
    description='查询hypixel游戏数据插件',
    usage=utils.usage,
    type='application',
    config=Config,
    homepage='https://github.com/Reversedeer/nonebot_plugin_hyp',
    supported_adapters={'~onebot.v11'},
    extra={
        'author': 'Reversedeer',
        'version': '0.0.4',
        'priority': 10,
        'email': 'ysjvillmark@gmail.com',
    },
)
