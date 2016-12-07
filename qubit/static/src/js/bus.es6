import $ from 'jquery'
import Bacon from 'baconjs'

$.fn.asEventStream = Bacon.$.asEventStream
export var keyUpStream = $(document).asEventStream('keyup').map(e => {return e.keyCode})
export var clickStream = $(document).asEventStream('click').map(e => {return e.target.className})
export var socketStream = new Bacon.Bus()

export class SocketBus {
    constructor(uri) {
        var self = this
        self.reader = new FileReader()
        self.ws = new WebSocket(uri)
        self.bus = new Bacon.Bus()
        self.ws.onmessage = function(msg) {
            self.reader.readAsText(msg.data)
        }
        self.reader.addEventListener('loadend', function() {
            self.bus.push(reader.result)
        })
    }
}
