from django.utils import timezone
from fritzconnection import FritzConnection


class LazyFritzConnection:
    fc = None
    last_connection=None



    def __call__(self) -> FritzConnection:
        if self.fc is None:
            self.fc = FritzConnection()
            self.last_connection = timezone.now()
        return self.fc


get_fritz_connection = LazyFritzConnection()
