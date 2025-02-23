# pylint: disable=missing-module-docstring
class User:
    """
    We define the structure of an user here.
    """

    def __init__(self, user_id: str, create_at: int, status: str):
        """
        Params:
            user_id (str): user's id.
            create_at (int): the timestamp of user's creation.
            status (str): the status of user.
        """
        self._user_id = user_id
        self._create_at = create_at
        self._status = status

    @property
    def user_id(self):
        """The user_id property."""
        return self._user_id

    @property
    def create_at(self):
        """The create_at property."""
        return self._create_at

    @property
    def status(self):
        """The status property."""
        return self._status

    def to_item(self):
        """
        Convert object into items format for dynamoDB.
        """
        return {
            'user_id': self._user_id,
            'create_at': self._create_at,
            'status': self._status
        }
