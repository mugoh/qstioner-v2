from .abstract_model import AbstractModel
from ..database.queries import *


class QuestionModel(AbstractModel):

    def __init__(self, **kwargs):

        super().__init__()
        self.title = kwargs['title']
        self.body = kwargs['body']
        self.meetup = kwargs['meetup']
        self.user = kwargs.get('user')

        self._votes = 0

    @property
    def votes(self):
        return self._votes

    @votes.setter
    def votes(self, value):
        raise AttributeError("Oops! You are not allowed to do that")

    def update_votes(self, add=True):
        if not add:
            self._votes -= 1
        else:
            self._votes += 1

    def save(self):
        """
            Saves question to the present record
            holding all questions
        """
        return super().save(CREATE_QUESTION, (self.title,
                                              self.body,
                                              self.meetup,
                                              self.user,
                                              self._votes,
                                              self.created_at
                                              ))

    def dictify(self):
        """
            Returns a dictionary of the question instance
        """

        return {
            "title": self.title,
            "body": self.body,
            "meetup": self.meetup,
            "user": self.user,
            "votes": self.votes
        }

        #
        # Searches

    @classmethod
    def get_all_questions(cls):
        """
            Converts all present question objects to a
            dictionary and sends them in a list envelope
        """
        return [question.dictify() for question in questions]

    @classmethod
    def get_by_id(cls, given_id, obj=False):
        """
            Searches and returns a question instance with
            an 'id' attribute matching the given id.
            Default return value is None.
        """

        # Send an instance or a dict item

        if obj:
            that_question = [question for question in questions
                             if getattr(question, 'id') == given_id]
        elif not obj:
            that_question = [question.dictify() for question in questions
                             if getattr(question, 'id') == given_id]

        return that_question[0] if that_question else None

    @classmethod
    def verify_existence(cls, question_object):
        """
            Helps minimize on  questions duplicity.
            Ensures that for each question, a question
            isn't re-created with the same data
        """
        return super().get_by_name(VERIFY_QUESTION,
                                   (question_object.title,
                                    question_object.body,
                                    question_object.meetup
                                    ))

    def __repr__(self):
        return '{title} {body} {meetup} {user}'.format(**self.dictify())
