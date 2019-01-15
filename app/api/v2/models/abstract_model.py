"""
    This file contains an abstract bodel class.
    All models inherit common attributes and behaviours from this model.

"""
import datetime
import pytz

from ..database.database import query_db


class AbstractModel:

    def __init__(self, object_data):
        self.created_at = self.get_utc_local()
        self.id = int

    def get_utc_local(self):
        local_t_zone = pytz.timezone('Africa/Nairobi')

        return local_t_zone.localize(
            datetime.datetime.now(), is_dst=None).isoformat()

    def save(self, statement, values):
        return query_db(statement, values, one=True)
