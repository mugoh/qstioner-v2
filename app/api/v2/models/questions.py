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
            On a second identical vote, the state for this user id becomes
            'not voted'

        """

        # Check if user has upvoted or downvoted before

        reupvote = None
        redownvote = None

        _downvoted = super().get_by_name(
            GET_VOTED_QUESTION, (user_id, q_id, 'downvoted'))
        _upvoted = super().get_by_name(GET_VOTED_QUESTION, (
            user_id, q_id, 'upvoted'))

        # Delete present vote record

        if add and _upvoted:
            super().delete(DELETE_VOTED_QUSER, _upvoted)
            reupvote = True
        elif not add and _downvoted:
            super().delete(DELETE_VOTED_QUSER, _downvoted)
            redownvote = True

        # Get current vote count
        stored_votes = super().get_by_id(GET_QUESTION_VOTES, (q_id,))[0]

        # If not a re-vote, update vote, and store the user
        # and question IDs

        if not reupvote and not redownvote:
            if not add:
                self.save_vote(CREATE_QUESTION_VOTE,
                               (user_id, q_id, 'downvoted'))
                self.alter_votes(stored_votes - 1)

            # Upvote and save user and Question id
            else:
                self.alter_votes(stored_votes + 1)
                self.save_vote(CREATE_QUESTION_VOTE,
                               (user_id, q_id, 'upvoted'))

        # For revotes, just clear the present vote

        elif reupvote:
            self.alter_votes(stored_votes - 1)
        elif redownvote:
            self.alter_votes(stored_votes + 1)

        super().update(
            UPDATE_QUESTION_VOTES, (self.votes, q_id))

        return QuestionModel.get_by_id(q_id)

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

    def save_vote(self, query, vote):
        """
            Saves a vote record to the votes table
        """
        return super().save(query, vote)

    def alter_votes(self, stored_votes):
        """
            Updates the instance vote attribute to match the passed argument
        """
        self._votes = stored_votes

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


keys = ["id", "title", "body",
        "meetup", "user", "votes", "created_at"]
