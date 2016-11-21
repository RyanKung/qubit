import $ from 'jquery'
import Bacon from 'baconjs'


export var bus = new Bacon.Bus()
$.fn.asEventStream = Bacon.$.asEventStream
export var keyUpStream = $(document).asEventStream('keyup').map(e => {return e.keyCode})
export var clickStream = $(document).asEventStream('click').map(e => {return e.target.className})
export var socketStream = new Bacon.Bus()
var ws = new WebSocket("ws://" + window.location.host + "/qubit/subscribe/");
var reader = new FileReader()
ws.onmessage = function(msg) {
    reader.addEventListener("loadend", function() {
        socketStream.push(reader.result)
    })
    reader.readAsText(msg.data)
}
