from .abstract_model import AbstractModel
from ..database.queries import *


class QuestionModel(AbstractModel):

    def __init__(self, **kwargs):

        super().__init__()
        self.title = kwargs['title']
        self.body = kwargs['body']
        self.meetup = kwargs['meetup']
        self.user = kwargs.get('user')
        self.id = kwargs.get('id')

        self._votes = 0

    @property
    def votes(self):
        return self._votes

    @votes.setter
    def votes(self, value):
        raise AttributeError("Oops! You are not allowed to do that")

    def update_votes(self, q_id, user_id, add=True):
        """
            Changes the vote count of a question.
            This method checks if the given user id has placed a simliar
            vote to that question id.
            On a second identical vote, the state for thisuser id becomes
            'not voted'

        """

        # Keep id of voted users and question in table

        # Check if user has upvoted or downvoted before

        _downvoted = super().get_by_name(
            GET_VOTED_QUESTION, (user_id, q_id, 'downvoted'))
        _upvoted = super().get_by_name(GET_VOTED_QUESTION, (
            user_id, q_id, 'upvoted'))

        # Delete predent vote record
        if _upvoted or _downvoted:

            if add and _upvoted:
                super().delete(DELETE_VOTED_QUSER, _upvoted)
                add = False
            elif not add and _downvoted:
                super().delete(DELETE_VOTED_QUSER, _downvoted)
                add = True

        stored_votes = super().get_by_id(GET_QUESTION_VOTES, (q_id,))[0]

        if not add:
            super().save(CREATE_QUESTION_VOTE,
                         (user_id, q_id, 'downvoted'))
            self._votes = stored_votes - 1
        else:
            self._votes = stored_votes + 1
            super().save(CREATE_QUESTION_VOTE,
                         (user_id, q_id, 'upvoted'))
        super().update(
            UPDATE_QUESTION_VOTES, (self.votes, q_id))
        voted = super().get_by_id(GET_QUESTION_BY_ID, (q_id,))

        return super().zipToDict(keys, voted, single=True)

    def save(self):
        """
            Saves a question to a new row in
            the QUESTIONS table
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
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "meetup": self.meetup,
            "user": self.user,
            "votes": self.votes,
            "created_at": self.created_at
        }

        #
        # Searches

    @classmethod
    def get_by_id(cls, given_id, obj=False):
        """
            Searches and returns a question instance
            or dict object an 'id' attribute matching
            the given id.
            Default return value is None.
        """

        # Send an instance or a dict item

        _question = super().get_by_id(GET_QUESTION_BY_ID, (given_id,))

        if _question and not obj:
            # A request for a dictionary
            return cls.zipToDict(keys, _question, single=True)

        elif _question and obj:
            # Give an instance of that question
            return QuestionModel(**cls.zipToDict(keys, _question,
                                                 single=True))
        return None

    @classmethod
    def verify_existence(cls, question_object):
        """
            Helps minimize on questions records duplicity.
            Ensures that for each question, a question
            isn't re-created with the same data.
        """
        return super().get_by_name(VERIFY_QUESTION,
                                   (question_object.title,
                                    question_object.body,
                                    question_object.meetup
                                    ))

    def __repr__(self):
        return '{title} {body} {meetup} {user}'.format(**self.dictify())


keys = ["id", "title", "body",
        "meetup", "user", "votes", "created_at"]
