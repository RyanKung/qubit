from .eventsocket import EventSocket, QubitSocket

__all__ = ['middleware']

middleware = [EventSocket, QubitSocket]
