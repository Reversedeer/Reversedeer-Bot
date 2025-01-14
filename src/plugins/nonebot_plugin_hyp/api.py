"""API及数据处理"""

import time
from typing import Literal
import asyncio

import httpx
from nonebot import get_plugin_config
from nonebot.log import logger

from .utils import Config

plugin_config = get_plugin_config(Config)


class Api:
    def __init__(self) -> None:
        self.mojang_profile = 'https://api.mojang.com/users/profiles/minecraft/'
        self.mojang_session = 'https://sessionserver.mojang.com/session/minecraft/profile/'
        self.hypixel_key = 'https://api.hypixel.net/key?key={}'
        self.hypixel_counts = 'https://api.hypixel.net/counts?key={}'
        self.hypixel_player = 'https://api.hypixel.net/player?key={}&uuid={}'
        self.hypixel_status = 'https://api.hypixel.net/status?key={}&uuid={}'
        self.hypixel_friends = 'https://api.hypixel.net/friends?key={}&uuid={}'
        self.hypixel_guild_name = 'https://api.hypixel.net/guild?key={}&name={}'
        self.hypixel_guild_player = 'https://api.hypixel.net/guild?key={}&player={}'
        self.hypixel_recentgames = 'https://api.hypixel.net/recentgames?key={}&uuid={}'
        self.hypixel_punishmentstats = 'https://api.hypixel.net/punishmentstats?key={}'
        self.antisniper_denick = 'https://api.antisniper.net/denick?key={}&nick={}'
        self.antisniper_findnick = 'https://api.antisniper.net/findnick?key={}&name={}'
        self.antisniper_winstreak = 'https://api.antisniper.net/winstreak?key={}&name={}'
        self.optifine_cape = 'http://s.optifine.net/capes/{}.png'
        self.optifine_format = 'https://optifine.net/banners&&'
        self.optifine_banner = 'http://optifine.net/showBanner?format={}&valign={}'
        self.max_retries = 3
        self.HTTP_STATUS_OK = 200
        self.HTTP_STATUS_NOT_FOUND = 400
        self.HTTP_STATUS_FORBIDDEN = 403
        self.HTPP_STATUS_NOT_FOUNDMC = 404
        self.HTTP_STATUS_TOO_MANY_REQUESTS = 429

    async def player_data(self, uid: str) -> dict:
        """初始化获取玩家数据"""
        mcdata: dict[str, str] = await self.get_mc_data(uid) or {}
        (
            player_data,
            player_status,
        ) = await asyncio.gather(
            self.get_player_data(mcdata),
            self.get_player_status(mcdata),
        )
        return {
            'player_data': player_data,
            'player_status': player_status,
        }

    async def get_player_data(self, mcdata: dict) -> dict[str, str]:
        """获取玩家hypixel游戏数据"""
        uuid = mcdata.get('id')
        apikey: str = plugin_config.hypixel_apikey
        url: str = self.hypixel_player.format(apikey, uuid)
        error_messages = {
            self.HTTP_STATUS_NOT_FOUND: '不存在此玩家数据或丢失',
            self.HTTP_STATUS_FORBIDDEN: '少密钥或此密钥无效',
            self.HTTP_STATUS_TOO_MANY_REQUESTS: '超出API请求次数限制',
        }
        async with httpx.AsyncClient() as client:
            for attempt in range(self.max_retries):
                try:
                    res: httpx.Response = await asyncio.wait_for(client.get(url, timeout=10), timeout=10)
                    break
                except httpx.RequestError as exc:
                    logger.error(f'获取玩家hypixel游戏数据时请求超时：{exc}')
                    if attempt == self.max_retries - 1:
                        return {'e': '获取玩家数据时发生未知错误，请稍后重试！'}
                    await asyncio.sleep(2**attempt)
            else:
                return {'e': '获取玩家数据时发生未知错误，请稍后重试！'}
            if res.status_code == self.HTTP_STATUS_OK:
                return res.json().get('player')
            error_message = error_messages.get(res.status_code, '未知错误')
            logger.error(f'获取玩家hypixel游戏数据时发生错误：{error_message}')
            return {'e': error_message}

        return {'e': '获取玩家数据时发生未知错误，请稍后重试！'}

    async def get_player_status(self, mcdata: dict) -> dict[str, str]:
        """获取玩家hypixel状态信息"""
        uuid = mcdata.get('id')
        apikey: str = plugin_config.hypixel_apikey
        url: str = self.hypixel_status.format(apikey, uuid)

        error_messages = {
            self.HTTP_STATUS_NOT_FOUND: '不存在此玩家数据或丢失',
            self.HTTP_STATUS_FORBIDDEN: '缺少密钥或此密钥无效',
            self.HTTP_STATUS_TOO_MANY_REQUESTS: '超出API请求次数限制',
        }
        async with httpx.AsyncClient() as client:
            for attempt in range(self.max_retries):
                try:
                    res: httpx.Response = await asyncio.wait_for(client.get(url, timeout=10), timeout=10)
                    break
                except httpx.RequestError as exc:
                    logger.error(f'获取玩家hypixel状态信息时请求超时：{exc}')
                    if attempt == self.max_retries - 1:
                        return {'e': '获取玩家数据时发生未知错误，请稍后重试！'}
                    await asyncio.sleep(2**attempt)
            else:
                return {'e': '获取玩家数据时发生未知错误，请稍后重试！'}
            if res.status_code == self.HTTP_STATUS_OK:
                return {'online': res.json().get('session', {}).get('online')}
            error_message = error_messages.get(res.status_code, '未知错误')
            logger.error(f'获取玩家hypixel状态信息时发生错误：{error_message}')
            return {'e': error_message}
        return {'e': '获取玩家数据时发生未知错误，请稍后重试！'}

    async def get_mc_data(self, uid: str) -> dict[str, str] | None:
        """获取玩家minecraft信息"""
        try:
            async with httpx.AsyncClient() as client:
                res: httpx.Response = await client.get(self.mojang_profile + uid, timeout=10)
                if res.status_code == self.HTTP_STATUS_OK:
                    return res.json()
                if res.status_code == self.HTPP_STATUS_NOT_FOUNDMC:
                    logger.error('获取玩家minecraft信息时：不存在此玩家数据或数据丢失')
                    return {'e': '玩家数据不存在或数据丢失，请检查 ID 是否正确！'}
        except httpx.RequestError as exc:
            logger.error(f'获取玩家minecraft信息请求超时:{exc}请稍后再试')
            return {'e': '请求超时，请稍后重试！'}

    @staticmethod
    async def get_player_online(data_b: str) -> Literal['在线', '离线']:
        """获取玩家在线状态"""
        online: str = data_b
        return '在线' if online else '离线'

    @staticmethod
    async def get_player_rack(data_a: dict) -> str:
        rank_id: str = data_a.get('newPackageRank', '')
        """获取玩家rank"""
        if rank_id in ('VIP', 'MVP'):
            rank = f'[{rank_id}]'
        elif rank_id in ('VIP_PLUS', 'MVP_PLUS'):
            rank: str = f'[{rank_id.replace("_PLUS", "+")}]'
        else:
            rank = '无'
        return rank

    @staticmethod
    async def get_login_time(player_time: int) -> str:
        """获取玩家上线时间"""
        if player_time is not None:
            time_array = time.localtime(player_time / 1000)
            last_login: str = time.strftime('%Y-%m-%d %H:%M:%S', time_array)
        else:
            last_login = '对方隐藏了最后的上线时间'
        return last_login

    @staticmethod
    async def get_player_level(xp: str) -> int:
        """获取玩家等级"""
        if xp is not None:
            prefix = -3.5
            const = 12.25
            divides = 0.0008
            try:
                lv = int((divides * int(xp) + const) ** 0.5 + prefix + 1)
                level: int = lv
            except ValueError:
                level = 0
        else:
            level = 0
        return level

    @staticmethod
    async def get_player_skywars_level(level: str) -> str:
        """获取skywars等级"""
        level_: str = level[2:-1]  # 去掉颜色代码和 '⋆'
        return level_ + '⋆'

    @staticmethod
    async def get_hypixel_bedwars_level(exp: int) -> dict:
        """计算 Hypixel 起床战争等级和经验进度"""
        level_exp_requirements: list[int] = [
            500,
            1000,
            2000,
            3500,
        ]  # 每个星级的经验需求
        max_level_exp = 487_000  # 每轮循环需要的总经验
        post_3_level_exp = 5000  # 3✫之后每个等级需要的经验

        # 等级与进度计算函数
        def calculate_progress(exp: int, thresholds: list) -> tuple:
            """
            根据经验值和经验阈值列表计算等级和经验进度
            """
            level = 0
            for req in thresholds:
                if exp < req:
                    break
                exp -= req
                level += 1
            return level, exp

        # 小于 7000 的等级和进度计算
        if exp < sum(level_exp_requirements):
            level, remaining_exp = calculate_progress(exp, level_exp_requirements)
            level_str = f'{level}✫'
            next_level_exp = f'{remaining_exp}/{level_exp_requirements[level]}'
        else:
            # 7000 以上的递增星级
            exp -= sum(level_exp_requirements)
            if exp < max_level_exp:
                add_level: int = exp // post_3_level_exp
                remaining_exp: int = exp % post_3_level_exp
                level: int = 4 + add_level
                level_str = f'{level}✫'
                next_level_exp: str = f'{remaining_exp}/{post_3_level_exp}'
            else:  # 超过 max_level_exp 的特殊循环处理
                loop_count: int = exp // max_level_exp  # 计算循环次数
                surplus_exp: int = exp % max_level_exp  # 当前循环内的剩余经验
                base_level: int = loop_count * 100  # 每轮加 100 星
                loop_level, remaining_exp = calculate_progress(
                    surplus_exp,
                    level_exp_requirements + [post_3_level_exp] * 100,
                )
                level_str: str = f'{base_level + loop_level}✫'
                next_level_exp = (
                    f'{remaining_exp}/{post_3_level_exp if loop_level >= 4 else level_exp_requirements[loop_level]}'  # noqa: PLR2004
                )
        return {
            'bw_level': level_str,
            'bw_experience': next_level_exp,
        }

    async def get_hypixel_data(self, data_a: dict) -> dict:
        """获取hypixel基本信息"""
        first_login = data_a.get('firstLogin')
        last_login = data_a.get('lastLogin')
        last_logout = data_a.get('lastLogout')
        network_exp = data_a.get('networkExp')

        return {
            'karma': data_a.get('karma'),
            'rank': await self.get_player_rack(data_a),
            'first_login': await self.get_login_time(first_login) if first_login is not None else '未知',
            'last_login': await self.get_login_time(last_login) if last_login is not None else '未知',
            'level': await self.get_player_level(network_exp) if network_exp is not None else '未知',
            'achievementPoints': data_a.get('achievementPoints'),  # 成就
            'quest_master': data_a.get('achievements', {}).get('general_quest_master'),  # 任务
            'challenger': data_a.get('achievements', {}).get('general_challenger'),  # 挑战
            'general_wins': data_a.get('achievements', {}).get('general_wins'),  # 小游戏胜场
            'general_coins': data_a.get('achievements', {}).get('general_coins'),  # 小游戏硬币
            'silver': data_a.get('seasonal', {}).get('silver'),  # 活动银币
            'total_tributes': data_a.get('tourney', {}).get('total_tributes'),  # 战魂
            'language': data_a.get('userLanguage'),
            'lastLogout': await self.get_login_time(last_logout) if last_logout is not None else '未知',  # 上次退出
            'recentgame': data_a.get('mostRecentGameType'),  # 最近游戏
        }

    async def get_players_skywars(self, data_a: dict) -> dict:
        """获取Skywars数据"""
        stats_data = data_a.get('stats')
        if not stats_data:
            logger.error('Stats 数据不存在')
            return {'error': 'Stats 数据不存在'}
        skywars_data = stats_data.get('SkyWars')
        if not skywars_data:
            logger.error('Skywars 数据不存在')
            return {'error': 'Skywars 数据不存在'}
        # 字段映射到变量
        fields = {
            'sw_level': await self.get_player_skywars_level(skywars_data.get('levelFormatted')),
            'sw_experience': skywars_data.get('skywars_experience', 0),
            'sw_coins': skywars_data.get('coins', 0),
            'sw_kills': skywars_data.get('kills', 0),
            'sw_deaths': skywars_data.get('deaths', 1),  # 避免死亡为 0 时计算崩溃
            'sw_wins': skywars_data.get('wins', 0),
            'sw_losses': skywars_data.get('losses', 1),  # 避免失败为 0 时计算崩溃
            'sw_souls': skywars_data.get('souls', 0),
            'sw_lastMode': skywars_data.get('lastMode', '未知'),
            'sw_games': skywars_data.get('games_played_skywars', 0),
            'sw_assists': skywars_data.get('assists', 0),
            'sw_cosmetic_tokens': skywars_data.get('cosmetic_tokens', 0),
            'sw_fastest_win': skywars_data.get('fastest_win', 0),
            'sw_win_streak': skywars_data.get('win_streak', 0),
            'sw_time_played': skywars_data.get('time_played', 0),
        }
        # 计算 K/D 和胜率比
        fields['SW_K_D'] = round(
            fields['sw_kills'] / fields['sw_deaths'],
            3,
        )
        fields['SW_W_L'] = round(
            fields['sw_wins'] / fields['sw_losses'],
            3,
        )
        return fields

    async def get_players_bedwars(self, data_a: dict) -> dict:
        """获取bedwars数据"""
        stats_data = data_a.get('stats')
        if not stats_data:
            logger.error('Stats 数据不存在')
            return {'error': 'Stats 数据不存在'}
        bedwars_data = stats_data.get('Bedwars')
        if not bedwars_data:
            logger.error('Bedwars 数据不存在')
            return {'error': 'Bedwars 数据不存在'}
        # 通过 Hypixel API 计算等级和经验
        data_b = await api.get_hypixel_bedwars_level(int(bedwars_data.get('Experience', 0)))
        # 字段映射到变量
        fields = {
            'bw_level': data_b.get('bw_level', 0),
            'bw_experience': data_b.get('bw_experience', 0),
            'bw_coin': bedwars_data.get('coins', 0),
            'winstreak': bedwars_data.get('winstreak', 0),
            'break_bed': bedwars_data.get('beds_broken_bedwars', 0),
            'lost_bed': bedwars_data.get('beds_lost_bedwars', 1),  # 避免为 0
            'bw_win': bedwars_data.get('wins_bedwars', 0),
            'bw_losses': bedwars_data.get('losses_bedwars', 1),  # 避免为 0
            'bw_kill': bedwars_data.get('kills_bedwars', 0),
            'bw_death': bedwars_data.get('deaths_bedwars', 1),  # 避免为 0
            'bw_final_kill': bedwars_data.get('final_kills_bedwars', 0),
            'bw_final_death': bedwars_data.get('final_deaths_bedwars', 1),  # 避免为 0
            'bw_iron': bedwars_data.get('iron_resources_collected_bedwars', 0),
            'bw_gold': bedwars_data.get('gold_resources_collected_bedwars', 0),
            'bw_diamond': bedwars_data.get('diamond_resources_collected_bedwars', 0),
            'bw_emerald': bedwars_data.get('emerald_resources_collected_bedwars', 0),
        }
        # 计算各类比值
        fields['BBLR'] = round(fields['break_bed'] / fields['lost_bed'], 3)
        fields['W_L'] = round(fields['bw_win'] / fields['bw_losses'], 3)
        fields['K_D'] = round(fields['bw_kill'] / fields['bw_death'], 3)
        fields['FKDR'] = round(fields['bw_final_kill'] / fields['bw_final_death'], 3)

        return fields


api = Api()
