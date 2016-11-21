import $ from 'jquery'
import Bacon from 'baconjs'

var ws = new WebSocket("ws://" + window.location.host + "/qubit/subscribe/");
var reader = new FileReader()

$.fn.asEventStream = Bacon.$.asEventStream
export var keyUpStream = $(document).asEventStream('keyup').map(e => {return e.keyCode})
export var clickStream = $(document).asEventStream('click').map(e => {return e.target.className})
export var socketStream = new Bacon.Bus()

ws.onmessage = function(msg) {
    reader.addEventListener("loadend", function() {
        socketStream.push(reader.result)
    })
    reader.readAsText(msg.data)
}
window.onbeforeunload = function(e) {
    ws.close()
}
