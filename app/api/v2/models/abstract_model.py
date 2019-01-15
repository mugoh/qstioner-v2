"""
    This file contains an abstract bodel class.
    All models inherit common attributes and behaviours from this model.

"""
import datetime
import pytz


class AbstractModel:

    def __init__(self, object_data):
        self.created_at = self.get_utc_local()
        self.id = len(object_data) + 1

    def get_utc_local(self):
        local_t_zone = pytz.timezone('Africa/Nairobi')

        return local_t_zone.localize(
            datetime.datetime.now(), is_dst=None).isoformat()
