# pylint: disable=missing-module-docstring
class Log:
    """
    We defined structure of a log here.
    """

    def __init__(
            self,
            user_id: str, input_: str, output: str, timestamp: int):
        """
        Params:
            user_id (str): User's id.
            input_ (str): the user's input to gpt.
            output (str): the response from gpt.
            timestamp (int): the timestamp of log. 
        """
        self._user_id = user_id
        self._input = input_
        self._output = output
        self._timestamp = timestamp

    @property
    def user_id(self):
        """The user_id property."""
        return self._user_id

    @property
    def input_(self):
        """The _input property."""
        return self._input

    @property
    def output(self):
        """The output property."""
        return self._output

    @property
    def timestamp(self):
        """The timestamp property."""
        return self._timestamp

    def to_item(self):
        """
        Convert object into items format for dynamoDB.
        """
        return {
            'user_id': self._user_id,
            'input': self._input,
            'output': self._output,
            'timestamp': self._timestamp
        }
