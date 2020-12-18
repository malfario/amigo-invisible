from typing import Any


class Notifier:
    """Basic interface for custom notifiers"""

    async def send_notification(self, recipient: str, message: Any):
        raise NotImplementedError('Subclasses must implement this method')
