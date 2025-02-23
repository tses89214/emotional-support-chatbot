# pylint: disable=missing-module-docstring
class Prompt:
    """
    We defined structure of a prompt here.
    """

    def __init__(
            self,
            user_id: str, prompt: str,
            valid_from: int, valid_to: int,
            is_current: bool):
        """
        Params:
            user_id (str): User's id.
            prompt (str): the command we gave gpt.
            valid_from (int): the start time of the prompt.
            valid_to (int): the end time of the prompt.
            is_current (bool): whether the prompt is current.
        """
        self._user_id = user_id
        self._prompt = prompt
        self._valid_from = valid_from
        self._valid_to = valid_to
        self._is_current = is_current

    @property
    def user_id(self):
        """The user_id property."""
        return self._user_id

    @property
    def prompt(self):
        """The prompt property."""
        return self._prompt

    @property
    def valid_from(self):
        """The valid_from property."""
        return self._valid_from

    @property
    def valid_to(self):
        """The valid_to property."""
        return self._valid_to

    @property
    def is_current(self):
        """The is_current property."""
        return self._is_current

    def to_item(self):
        """
        Convert object into items format for dynamoDB.
        """
        return {
            'user_id': self._user_id,
            'prompt': self._prompt,
            'valid_from': self._valid_from,
            'valid_to': self._valid_to,
            'is_current': self._is_current
        }
