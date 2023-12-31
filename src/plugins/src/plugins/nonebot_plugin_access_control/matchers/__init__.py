from argparse import Namespace
from io import StringIO
from typing import cast

from nonebot import on_shell_command
from nonebot.exception import ParserExit
from nonebot.internal.adapter import Event
from nonebot.internal.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State

from .handle_error import handle_error
from .parser import parser
from ..service import get_services_by_subject, Service, get_service_by_qualified_name
from ..utils.tree import get_tree_summary

cmd = on_shell_command("ac", parser=parser, permission=SUPERUSER)


@cmd.handle()
@handle_error()
async def _(matcher: Matcher, event: Event, state: T_State):
    args = state["_args"]
    if isinstance(args, ParserExit):
        await matcher.finish(args.message)

    args = cast(Namespace, args)

    if args.subcommand == 'subject':
        if args.action == 'ls':
            if args.target == 'service':
                await handle_subject_ls_service(matcher, args.subject)
        elif args.action == 'allow':
            if args.target == 'service':
                await handle_subject_allow_service(matcher, args.subject, args.service)
        elif args.action == 'deny':
            if args.target == 'service':
                await handle_subject_deny_service(matcher, args.subject, args.service)
        elif args.action == 'remove':
            if args.target == 'service':
                await handle_subject_remove_service(matcher, args.subject, args.service)
    elif args.subcommand == 'service':
        if args.action == 'ls':
            if args.target is None:
                await handle_service_ls_subservice(matcher, args.service)
            elif args.target == 'subject':
                await handle_service_ls_subject(matcher, args.service)


async def handle_subject_ls_service(matcher: Matcher, subject: str):
    services = [x async for x in get_services_by_subject(subject)]
    if len(services) != 0:
        # 按照先allow再deny排序
        services = sorted(services, key=lambda x: x[1], reverse=True)
        msg = '\n'.join(map(lambda x: x[0].qualified_name + (' allow' if x[1] else ' deny'), services))
    else:
        msg = "empty"
    await matcher.send(msg)


async def _get_service(matcher: Matcher, service_name: str) -> Service:
    service_name = get_service_by_qualified_name(service_name)

    if service_name is None:
        await matcher.finish("service not found")
    else:
        return service_name


async def handle_subject_allow_service(matcher: Matcher, subject: str, service: str):
    service = await _get_service(matcher, service)
    await service.set_permission(subject, True)
    await matcher.send("ok")


async def handle_subject_deny_service(matcher: Matcher, subject: str, service: str):
    service = await _get_service(matcher, service)
    await service.set_permission(subject, False)
    await matcher.send("ok")


async def handle_subject_remove_service(matcher: Matcher, subject: str, service: str):
    service = await _get_service(matcher, service)
    await service.remove_permission(subject)
    await matcher.send("ok")


async def handle_service_ls_subject(matcher: Matcher, service_name: str):
    permissions = {}
    service = await _get_service(matcher, service_name)

    while service is not None:
        async for subject, allow in service.get_permissions():
            permissions.setdefault(subject, (allow, service))
        service = service.parent

    if len(permissions) != 0:
        # 按照先allow再deny排序
        permissions = [(*permissions[k], k) for k in permissions]
        permissions = sorted(permissions, reverse=True)
        with StringIO() as sio:
            for allow, service, subject in permissions:
                sio.write(subject)
                if allow:
                    sio.write(" allow")
                else:
                    sio.write(" deny")

                if service.qualified_name != service_name:
                    sio.write(f" (inherited from {service.qualified_name})")
                sio.write('\n')
            msg = sio.getvalue().strip()
    else:
        msg = "empty"
    await matcher.send(msg)


async def handle_service_ls_subservice(matcher: Matcher, service_name: str):
    service = await _get_service(matcher, service_name)
    summary = get_tree_summary(service, lambda x: x.children, lambda x: x.name)
    await matcher.send(summary)
