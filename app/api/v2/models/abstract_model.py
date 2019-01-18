"""
    This file contains an abstract bodel class.
    All models inherit common attributes and behaviours from this model.

"""
import datetime
import pytz

from ..database.database import query_db


class AbstractModel:

    def __init__(self):
        self.created_at = self.get_utc_local()
        self.id = None

    def get_utc_local(self):
        local_t_zone = pytz.timezone('Africa/Nairobi')

        return local_t_zone.localize(
            datetime.datetime.now(), is_dst=None).isoformat()

    def save(self, statement, values):
        return query_db(statement, tuple(values), one=True)

    def delete(self, statement, values):
        return query_db(statement, values, rowcount=True)

    def update(self, statement, values):
        return query_db(statement, values, rowcount=True)

    @classmethod
    def get_by_name(cls, statement, value):
        return query_db(statement, value, one=True)

    @classmethod
    def get_by_id(cls, statement, value):
        return query_db(statement, value, one=True)

    @classmethod
    def get_all(cls, statement, values=None):
        if values:
            return query_db(statement, values, many=True)

        return query_db(statement, many=True)

    @classmethod
    def zipToDict(cls, keys, iters, single=False):
        """
            Returns key, value pairs for response ouputs in
            successful requests for record names and record data
            fetched from the database
        """
        if single:
            return dict(zip(keys, iters))

        return [dict(zip(keys, item)) for item in iters]
