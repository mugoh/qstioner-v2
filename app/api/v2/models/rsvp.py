from .abstract_model import AbstractModel
from ..database.queries import *


class RsvpModel(AbstractModel):

    def __init__(self, **kwargs):

        super().__init__()
        self.user = kwargs['user']
        self.meetup = kwargs['meetup']
        self.response = kwargs['response']

    def save(self):
        """
            Saves rsvp details to the present table
            holding all rsvps.
        """
        return super().save(CREATE_RSVP,
                            (self.meetup,
                             self.user,
                             self.response))

    @classmethod
    def get_for_user(cls, usr):
        """
            Retrieves all rsvps that match the current user's ID.
        """
        return cls.get_all(GET_USER_RSVPS, (usr,))

    @classmethod
    def verify_unique(cls, rsvp_object):
        """
            Helps in ensuring a user does not rsvp for
            the meetup twice with the same rsvp data.
        """
        return cls.get_by_name(VERIFY_RSVP,
                               (rsvp_object.meetup,
                                rsvp_object.user,
                                rsvp_object.response))
