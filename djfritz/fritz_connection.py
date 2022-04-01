import logging
import time

from django.utils import timezone
from fritzconnection import FritzConnection
from fritzconnection.core.exceptions import FritzActionFailedError, FritzConnectionException
from fritzconnection.lib.fritzbase import AbstractLibraryBase


logger = logging.getLogger(__name__)


class LazyFritzConnection:
    fc = None
    last_connection = None

    def __call__(self) -> FritzConnection:
        if self.fc is None:
            try:
                self.fc = FritzConnection()
            except FritzConnectionException as err:
                logger.error('Can not connect to FritzBox: %s', err)
            else:
                self.last_connection = timezone.now()
        return self.fc


get_fritz_connection = LazyFritzConnection()


class FritzHostFilter(AbstractLibraryBase):
    SERVICE = 'X_AVM-DE_HostFilter1'

    def _action(self, actionname, *, arguments=None, **kwargs):
        return self.fc.call_action(self.SERVICE, actionname, arguments=arguments, **kwargs)

    WAN_ACCESS_STATE_GRANTED = 'granted'
    WAN_ACCESS_STATE_DENIED = 'denied'
    WAN_ACCESS_STATE_ERROR = 'error'
    KNOWN_WAN_ACCESS_STATES = (
        # These states will the FritzBox return. If not -> use "unknown" below
        WAN_ACCESS_STATE_GRANTED,
        WAN_ACCESS_STATE_DENIED,
        WAN_ACCESS_STATE_ERROR,
    )
    WAN_ACCESS_STATE_UNKNOWN = 'unknown'

    def get_wan_access_state(self, ip):
        """
        Returns the state of WANAccess for the given LAN device’s IP address.
        States are:
            "granted" The LAN device has access to WAN.
            "denied" The LAN device has no access to WAN.
            "error" Something went wrong, the state could not yet be retrieved.

        Needs authenticated login to FritzBox.
        """
        raw_state = self._action('GetWANAccessByIP', NewIPv4Address=ip)
        state = raw_state['NewWANAccess']
        logger.info('GetWANAccessByIP: ip=%r has state=%r (Raw: %r)', ip, state, raw_state)
        if state not in self.KNOWN_WAN_ACCESS_STATES:
            return self.WAN_ACCESS_STATE_UNKNOWN
        return state

    def set_wan_access_state(self, ip: str, allow: bool) -> str:
        """
        Change the internet access for given device’s IP address.

            allow is True -> WAN access granted
            allow is False -> WAN access denied

        (Needs authenticated login to FritzBox.)
        """
        state_map = {
            True: (0, self.WAN_ACCESS_STATE_GRANTED),
            False: (1, self.WAN_ACCESS_STATE_DENIED),
        }
        new_disallow, expected_state = state_map[allow]

        logger.info('DisallowWANAccessByIP: Set disallow=%r for ip=%r', new_disallow, ip)
        self._action('DisallowWANAccessByIP', NewIPv4Address=ip, NewDisallow=new_disallow)

        state = None
        for sec in range(30, 1, -1):
            state = self.get_wan_access_state(ip=ip)
            if state != expected_state:
                logger.info(f'State {state} is not {expected_state}... (max wait {sec}sec.)')
                time.sleep(1)
            else:
                return state

        raise FritzActionFailedError(
            f'Setting WAN access for {ip} to {expected_state} failed, new state is: {state}'
        )

    def allow_wan_access(self, ip: str) -> str:
        """
        Set WAN access state to "granted" (Needs to be authenticated)
        """
        return self.set_wan_access_state(ip=ip, allow=True)

    def disallow_wan_access(self, ip: str) -> str:
        """
        Set WAN access state to "denied" (Needs to be authenticated)
        """
        return self.set_wan_access_state(ip=ip, allow=False)
