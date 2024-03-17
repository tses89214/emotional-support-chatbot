#pylint: disable=missing-module-docstring
class User:
    """
    We define the structure of an user here.
    """
    def __init__(self, user_id: str, prompt: str):
        """
        Params:
            user_id (str): user's id.
            prompt (str): the command we gave gpt.
        """
        self._user_id = user_id
        self._prompt = prompt

    @property
    def user_id(self):
        """The user_id property."""
        return self._user_id

    @property
    def prompt(self):
        """The prompt property."""
        return self._prompt

    @prompt.setter
    def set_prompt(self, new_prompt: str):
        """
        We allow user to set prompt.

        Params:
            prompt (str): The prompt want to set.
        """
        self._prompt = new_prompt

    def to_item(self):
        """
        Convert object into items format for dynamoDB.
        """
        return {
            'user_id': self._user_id,
            'prompt': self._prompt
        }
