from pulsar.apps import ws

__all___ = ['EventSocket', 'app']


class EventSocketHandler(ws.WS):

    def on_message(self, websocket, message):
        websocket.write(message)

EventSocket = ws.WebSocket('/qubit/eventsocket/', EventSocketHandler())
