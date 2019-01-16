"""
    Holds the model for the meetup resource
"""

from ..models.abstract_model import AbstractModel
from ..database.queries import *


class MeetUpModel(AbstractModel):

    def __init__(self, **kargs):

        super().__init__(meetups)
        self.location = kargs.get('location')
        self.images = kargs.get('images')
        self.topic = kargs.get('topic')
        self.happeningOn = kargs.get('happeningOn')
        self.tags = kargs.get('tags')

    def save(self):
        """
            Saves meetup instance to present records
        """
        super().save(CREATE MEETUP,
                     self.topic,
                     self.images,
                     self.location,
                     self.tags,
                     self.happeningOn)

    def dictify(self):
        """
            Returns a dictionary of the meetup instance
        """

        """return {
            "topic": self.topic,
            "location": self.location,
            "happeningOn": self.happeningOn,
            "tags": self.tags,
        }
        """
        return self.__dict__

        #
        # Searches

    @classmethod
    def get_by_id(cls, given_id, obj=False):
        """
            Searches and returns a meetup instance
            with an 'id' attribute matching the given id.
        """
        that_meetup = super().get_by_id(GET_MEETUP_BY_ID, (given_id,))
        self.zipToDict(that_meetup)

        if not obj:
            that_meetup = [meetup.dictify() for meetup in meetups
                           if getattr(meetup, 'id') == given_id]
        else:
            that_meetup = [meetup for meetup in meetups
                           if getattr(meetup, 'id') == given_id]

        return that_meetup[0] if that_meetup else None

    def delete(self):
        """
            Permanently removes a meetup from the records.
        """
        meetups.remove([x for x in meetups if x == self][0])

    def zipToDict(self, iterable):
        keys = ["topic", "images", "location", "happening_on",
                "tags"]
        return dict(zip(keys, iterable))

    @classmethod
    def verify_unique(cls, meetup_object):
        """
            Ensures a meetup isn't re-created with the
            same data
        """
        return any(super().get_by_name(VERIFY_MEETUP,
                                       meetup_object.__dict__.values()))

    def __repr__(self):
        return '{topic} {tags} {location}'.format(**self.dictify())


meetups = []  # Holds all meetups records
