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
