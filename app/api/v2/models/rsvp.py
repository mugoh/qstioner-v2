from .abstract_model import AbstractModel
from ..database.queries import *


class RsvpModel(AbstractModel):

    def __init__(self, **kwargs):

        super().__init__(rsvps)
        self.user = kwargs['user']
        self.meetup = kwargs['meetup']
        self.response = kwargs['response']

    def save(self):
        """
            Saves rsvp details to the present table
            holding all rsvps
        """
        return super().save(CREATE_RSVP,
                            (self.meetup,
                             self.user,
                             self.response))

    def dictify(self):
        """
            Returns a dictionary of the rsvp instance
            for readability of the rsvp's fields.
        """

        return {
            "response": self.response,
            "meetup": self.meetup,
            "user": self.user,
        }

        #
        # Searches

    @classmethod
    def get_all_rsvps(cls, obj=False):
        """
            Converts all present rsvp objects to a
            dictionary and sends them in a list envelope
        """
        if obj:
            return [rsvp for rsvp in rsvps]

        return [rsvp.dictify() for rsvp in rsvps]

    @classmethod
    def get_for_user(cls, usr):
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

    def __repr__(self):
        return '{meetup} {user}'.format(**self.dictify())
