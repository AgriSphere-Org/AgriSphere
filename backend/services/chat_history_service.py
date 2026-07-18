from typing import List


class ChatHistoryService:
    """
    Temporary in-memory chat history.

    Replace with PostgreSQL in production.
    """

    def __init__(self):

        self.history = []

    def add_message(
        self,
        role: str,
        message: str
    ):

        self.history.append({

            "role": role,

            "message": message

        })

    def get_history(self) -> List[dict]:

        return self.history

    def clear_history(self):

        self.history.clear()