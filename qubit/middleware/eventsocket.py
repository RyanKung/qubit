from pulsar.apps import ws
from qubit.io.redis import pubsub

__all___ = ['EventSocket', 'app']


class EventSocketHandler(ws.PubSubWS):

    def on_message(self, sck, msg):
        pass

EventSocket = ws.WebSocket('/qubit/subscribe/',
                           EventSocketHandler(pubsub, 'eventsocket'))
