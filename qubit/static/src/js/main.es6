import { SpoutView } from 'views/spout'
import React from 'react'
import ReactDOM from 'react-dom';
import { bus } from 'bus'


var mainView = (
        <div>
        <SpoutView></SpoutView>
        </div>
)
if (typeof window !== 'undefined') {
    ReactDOM.render(mainView, document.querySelector('.content .bd'))
}

var ws = new WebSocket("ws://127.0.0.1:8060/qubit/eventsocket/");
