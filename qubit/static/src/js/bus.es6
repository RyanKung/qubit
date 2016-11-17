import $ from 'jquery'
import Bacon from 'baconjs'
export var bus = new Bacon.Bus()
$.fn.asEventStream = Bacon.$.asEventStream
export var keyUpStream = $(document).asEventStream('keyup').map(e => {return e.keyCode})
export var clickStream = $(document).asEventStream('click').map(e => {return e.target.className})
