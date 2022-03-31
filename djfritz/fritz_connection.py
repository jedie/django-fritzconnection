import logging

from django.utils import timezone
from fritzconnection import FritzConnection
from fritzconnection.core.exceptions import FritzConnectionException
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

    def wan_access_state(self, ip):
        """
        Returns the state of WANAccess for the given LAN device’s IP address.
        States are:
            "granted" The LAN device has access to WAN.
            "denied" The LAN device has no access to WAN.
            "error" Something went wrong, the state could not yet be retrieved.

        Needs authenticated login to FritzBox.
        """
        return self._action('GetWANAccessByIP', NewIPv4Address=ip)

    def disallow_wan_access(self, ip: str, state: int) -> None:
        """
        Change the internet access for given device’s IP address.

            state == 0 -> access granted
            state == 1 -> access denied

        Needs authenticated login to FritzBox.
        """
        logger.info('DisallowWANAccessByIP ip=%r, state=%r', ip, state)
        assert state in (0, 1), 'Unknown state! (Can only be 0 or 1)'
        self._action('DisallowWANAccessByIP', NewIPv4Address=ip, NewDisallow=state)
