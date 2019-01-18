"""
    Holds the model for the meetup resource
"""

from ..models.abstract_model import AbstractModel
from ..database.queries import *

keys = ["id", "topic", "images", "location", "happeningOn",
        "tags"]


class MeetUpModel(AbstractModel):

    def __init__(self, **kargs):

        super().__init__()
        self.location = kargs.get('location')
        self.images = kargs.get('images')
        self.topic = kargs.get('topic')
        self.happeningOn = kargs.get('happeningOn')
        self.tags = kargs.get('tags')
        self.id = kargs.get('id')

    def save(self):
        """
            Saves meetup to present records
        """
        super().save(CREATE_MEETUP,
                     (self.topic,
                      self.images,
                      self.location,
                      self.happeningOn,
                      self.tags))

    def dictify(self):
        """
            Returns a dictionary of the meetup instance
        """

        data = {
            "topic": self.topic,
            "location": self.location,
            "happeningOn": self.happeningOn,
            "tags": self.tags,
        }

        if self.id:
            data.update({"id": self.id})

        return data

        #
        # Searches

    @classmethod
    def get_by_id(cls, given_id, obj=False):
        """
            Searches and returns a meetup instance
            with an 'id' attribute matching the given id.
        """
        that_meetup = super().get_by_id(GET_MEETUP_BY_ID, (given_id,))

        if that_meetup and not obj:
            # A request for a dictionary
            return MeetUpModel(**cls.zipToDict(keys, that_meetup, single=True)
                               ).dictify()

        elif that_meetup and obj:
            # Give an instance of that meetup
            return MeetUpModel(**cls.zipToDict(keys, that_meetup,
                                               single=True))

        return None

    @classmethod
    def verify_unique(cls, meetup_object):
        """
            Ensures a meetup isn't re-created with the
            same data
        """
        return super().get_by_name(VERIFY_MEETUP,
                                   (meetup_object.topic,
                                    meetup_object.tags,
                                    meetup_object.location))

    def __repr__(self):
        return '{topic} {tags} {location}'.format(**self.dictify())
