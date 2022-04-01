import logging
import time

import reversion
from bx_django_utils.humanize.time import human_timedelta
from bx_django_utils.models.manipulate import CreateOrUpdateResult, create_or_update2
from django.utils.translation import gettext as _
from fritzconnection.lib.fritzhosts import FritzHosts

from djfritz.fritz_connection import FritzHostFilter, get_fritz_connection
from djfritz.models import HostModel


logger = logging.getLogger(__name__)


def update_host(host: HostModel) -> CreateOrUpdateResult:
    mac_address: str = host.mac

    fc = get_fritz_connection()
    fh = FritzHosts(fc=fc)
    data = fh.get_specific_host_entry(mac_address=mac_address)

    ip_v4 = data['NewIPAddress']

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
        wan_access = fhf.get_wan_access_state(ip=ip_v4)
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
