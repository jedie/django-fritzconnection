import asyncio
import logging
import shutil
import socket
import time
from asyncio import StreamReader
from asyncio.subprocess import Process

import reversion
from asgiref.sync import async_to_sync, sync_to_async
from bx_django_utils.humanize.time import human_timedelta
from bx_django_utils.models.manipulate import CreateOrUpdateResult, create_or_update2
from django.contrib import messages
from django.utils.translation import gettext as _
from fritzconnection.core.exceptions import FritzConnectionException, FritzLookUpError
from fritzconnection.lib.fritzhosts import FritzHosts

from djfritz.fritz_connection import FritzHostFilter, get_fritz_connection
from djfritz.models import HostModel


logger = logging.getLogger(__name__)


def update_host(host: HostModel) -> CreateOrUpdateResult:
    mac_address: str = host.mac

    fc = get_fritz_connection()
    fh = FritzHosts(fc=fc)
    try:
        data = fh.get_specific_host_entry(mac_address=mac_address)
    except FritzLookUpError as err:
        logger.exception('Error updating %s: %s', host, err)
        raise

    ip_v4 = data['NewIPAddress']
    if not ip_v4:
        logger.warning('No IP from: %r', data)
        raise FritzLookUpError('Host IP is unknown! Cannot update host without IP!')

    fhf = FritzHostFilter(fc=fc)
    wan_access = fhf.get_wan_access_state(ip=ip_v4)

    with reversion.create_revision():
        result: CreateOrUpdateResult = create_or_update2(
            ModelClass=HostModel,
            lookup={'mac': mac_address},
            ip_v4=ip_v4,
            name=data['NewHostName'],
            last_status=data['NewActive'],
            interface_type=data['NewInterfaceType'] or None,
            address_source=data['NewAddressSource'],
            lease_time_remaining=data['NewLeaseTimeRemaining'],
            wan_access=wan_access,
        )
        if result.created:
            comment = 'Created'
        elif result.updated_fields:
            comment = f'Updated: {", ".join(result.updated_fields)}'
        else:
            comment = 'unchanged'

        logger.info('%s - %s', comment, result.instance)
        reversion.set_comment(comment)
    return result


def update_hosts():
    logger.info('start updating hosts...')
    start_time = time.monotonic()
    fc = get_fritz_connection()
    fh = FritzHosts(fc=fc)
    fhf = FritzHostFilter(fc=fc)
    hosts = fh.get_hosts_info()

    created = 0
    updated = 0
    unchanged = 0
    for host in hosts:

        ip_v4 = host['ip']
        if not ip_v4:
            logger.warning('No IP from: %r', host)
            continue

        try:
            wan_access = fhf.get_wan_access_state(ip=ip_v4)
        except FritzConnectionException as err:
            logger.exception('Error getting WAN access state for %r: %s', ip_v4, err)
            wan_access = FritzHostFilter.WAN_ACCESS_STATE_UNKNOWN
        else:
            logger.info('WAN access state for %r is: %r', ip_v4, wan_access)

        with reversion.create_revision():
            result: CreateOrUpdateResult = create_or_update2(
                ModelClass=HostModel,
                lookup={'mac': host['mac']},
                ip_v4=ip_v4,
                name=host['name'],
                last_status=host['status'],
                interface_type=host['interface_type'] or None,
                address_source=host['address_source'],
                lease_time_remaining=host['lease_time_remaining'],
                wan_access=wan_access,
            )
            if result.created:
                created += 1
                comment = 'Created'
            elif result.updated_fields:
                updated += 1
                comment = f'Updated: {", ".join(result.updated_fields)}'
            else:
                unchanged += 1
                comment = 'unchanged'

            logger.info('%s - %s', comment, result.instance)
            reversion.set_comment(comment)

    duration_str = human_timedelta(time.monotonic() - start_time)
    message = _(
        f'{created} hosts created, {updated} updated and {unchanged} not changed in {duration_str}'
    )
    return message


def set_wan_access_state(host: HostModel, allow: bool) -> CreateOrUpdateResult:
    """
    Set WAN access state for given "host" instance.
    """
    ip_v4: str = host.ip_v4
    if not ip_v4:
        raise RuntimeError('Host IP is unknown! Cannot change the WAN access state without IP!')

    fc = get_fritz_connection()
    fhf = FritzHostFilter(fc=fc)
    if allow:
        state = fhf.allow_wan_access(ip=ip_v4)
    else:
        state = fhf.disallow_wan_access(ip=ip_v4)

    result: CreateOrUpdateResult = create_or_update2(
        ModelClass=HostModel,
        lookup={'mac': host.mac},
        wan_access=state,
    )
    return result


def set_wan_access_with_messages(request, host: HostModel, allow: bool) -> None:
    try:
        result: CreateOrUpdateResult = set_wan_access_state(host=host, allow=allow)
    except FritzConnectionException as err:
        msg = f'Error set a new WAN access state to {host}: {err}'
        logger.exception(msg)
        messages.error(request, msg)
    else:
        if result.updated_fields:
            host.refresh_from_db()
            messages.success(request, f'{host} WAN access state changed to: {host.wan_access}')
        else:
            messages.info(request, f'{host} WAN access state unchanged.')


class SubprocessPing:
    ping_bin = None

    async def __call__(self, ip_address, count=1, timeout=1):
        if not self.ping_bin:
            self.ping_bin = shutil.which('ping')
            logger.info('Set ping executeable to: %r', self.ping_bin)
            if not self.ping_bin:
                raise FileNotFoundError('Executeable "ping" not found!')

        args = [self.ping_bin, '-c', str(count), '-W', str(timeout), ip_address]
        logger.info('Call ping: %r', args)

        process: Process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )

        returncode = await process.wait()
        logger.info('ping %r return code: %r', ip_address, returncode)

        stdout: StreamReader = process.stdout
        output = await stdout.read()
        output = output.decode('utf-8').strip()
        logger.info('ping %r output: %s', ip_address, output)

        @sync_to_async
        def get_mac_addresses(ip_address):
            return sorted(HostModel.objects.filter(ip_v4=ip_address).values_list('mac', flat=True))

        mac_addresses = await get_mac_addresses(ip_address)

        data = {
            'ip_address': ip_address,
            'mac_addresses': mac_addresses,
            'returncode': returncode,
            'output': output,
        }
        return data


subprocess_ping = SubprocessPing()


@async_to_sync
async def collect_host_info(names):
    async def collect(name):
        logger.info('Collect info for: %r', name)
        entry = {'name': name}
        try:
            fqdn = socket.getfqdn(name)
            entry['fqdn'] = fqdn

            (name, aliaslist, addresslist) = socket.gethostbyname_ex(fqdn)
            entry['aliaslist'] = aliaslist

            entry['ping_info'] = await asyncio.gather(
                *[subprocess_ping(ip_address, count=1, timeout=3) for ip_address in addresslist]
            )
        except Exception as err:
            logger.exception('%r error: %s', name, err)
            entry['error'] = err
        return entry

    data = await asyncio.gather(*[collect(name) for name in names])
    return data
