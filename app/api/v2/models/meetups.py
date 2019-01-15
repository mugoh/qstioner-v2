"""
    Holds the model for the meetup resource
"""

from ..models.abstract_model import AbstractModel


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
        meetups.append(self)

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
    def get_all_meetups(cls):
        """
            Converts all present meetup objects to a
            dictionary and sends them in a list envelope
        """
        return [meetup.dictify() for meetup in meetups]

    @classmethod
    def get_by_id(cls, given_id, obj=False):
        """
            Searches and returns a meetup instance
            with an 'id' attribute matching the given id.
        """
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

    @classmethod
    def verify_unique(cls, meetup_object):
        """
            Ensures a meetup isn't re-created with the
            same data
        """
        return any([meetup for meetup in meetups
                    if repr(meetup) == repr(meetup_object)])

    def __repr__(self):
        return '{topic} {tags} {location}'.format(**self.dictify())


meetups = []  # Holds all meetups records
