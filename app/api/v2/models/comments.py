from .abstract_model import AbstractModel
from ..database.queries import *


class CommentModel(AbstractModel):

    def __init__(self, **kwargs):

        super().__init__()
        self.user = kwargs['user']
        self.question = kwargs['question']
        self.body = kwargs['body']

    def save(self):
        """
            Saves comment details to the present table
            holding all comments.
        """
        return super().save(CREATE_COMMENT,
                            (self.question,
                             self.user,
                             self.body))

    @classmethod
    def get_for_user(cls, usr):
        """
            Retrieves all comments that match the current user's ID.
        """
        return cls.get_all(GET_USER_COMMENTS, (usr,))

    @classmethod
    def verify_unique(cls, comment_object):
        """
            Ensures a user does not comment to
            a question with the an already posted comment.
        """
        return cls.get_by_name(VERIFY_COMMENT,
                               (comment_object.question,
                                comment_object.user,
                                comment_object.body))
