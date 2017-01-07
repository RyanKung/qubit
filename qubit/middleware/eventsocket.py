from pulsar.apps import ws
from pulsar.apps.wsgi import route
from pulsar import ensure_future
from qubit.io.redis import pubsub
import logging

__all___ = ['QubitSocket']


class WebSocketRouter(ws.WebSocket):
    @route('/<int:qid>/', method='get')
    def qubit(self, request):
        qid = list(filter(bool, (request.path.split('/'))))[-1]
        request.qid = qid
        return super().get(request)


class PubSubWS(ws.WS):
    '''A :class:`.WS` handler with a publish-subscribe handler
    '''
    client = ws.PubSubClient

    def __init__(self, pubsub, channel):
        self.pubsub = pubsub
        self.channel = channel

    def on_open(self, websocket):
        qid = websocket.handshake.qid
        channel = self.channel % qid
        self.pubsub.add_client(self.client(websocket, channel))
        ensure_future(self.pubsub.subscribe(channel))
        logging.info(
            'New websocket opened. Add client to %s on "%s" channel',
            self.pubsub, self.channel)

    def write(self, websocket, message):
        print(message)
        websocket.write(message)


QubitSocket = WebSocketRouter('/qubit/subscribe', PubSubWS(pubsub, 'qubitsocket::%s'))
