import $ from 'jquery'
import Bacon from 'baconjs'

$.fn.asEventStream = Bacon.$.asEventStream
export var keyUpStream = $(document).asEventStream('keyup').map(e => {return e.keyCode})
export var clickStream = $(document).asEventStream('click').map(e => {return e.target.className})
export var bus = new Bacon.Bus()
export var updateBus = new Bacon.Bus()
export class SocketBus {
    constructor(uri) {
        var self = this
        self.reader = new FileReader()
        self.ws = new WebSocket(uri)
        self.bus = new Bacon.Bus()
        self.ws.onmessage = (msg) => {
            self.bus.push(JSON.parse(msg.data))
        }
    }
}
