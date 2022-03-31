import logging

from django.utils import timezone
from fritzconnection import FritzConnection
from fritzconnection.core.exceptions import FritzConnectionException


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
