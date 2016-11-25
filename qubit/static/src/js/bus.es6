import $ from 'jquery'
import Bacon from 'baconjs'

var ws = new WebSocket("ws://" + window.location.host + "/qubit/subscribe/1234/");
var reader = new FileReader()

$.fn.asEventStream = Bacon.$.asEventStream
export var keyUpStream = $(document).asEventStream('keyup').map(e => {return e.keyCode})
export var clickStream = $(document).asEventStream('click').map(e => {return e.target.className})
export var socketStream = new Bacon.Bus()
export var updatedSteam = socketStream.map(function(msg) {
    if (msg && msg.startsWith('qubit::updated::')) {
        let splited = msg.split('::')
        return {
            'qid': splited[2],
            'datum': JSON.parse(splited[3])
        }
    }
})

ws.onmessage = function(msg) {
    reader.addEventListener("loadend", function() {
        socketStream.push(reader.result)
    })
    reader.readAsText(msg.data)
}
window.onbeforeunload = function(e) {
    ws.close()
}
