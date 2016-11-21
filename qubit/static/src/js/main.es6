import { SpoutView } from 'views/spout'
import React from 'react'
import ReactDOM from 'react-dom';
import { bus } from 'bus'

export class MainView extends React.Component {
    render () {
        return (
         <div>
           <SpoutView></SpoutView>
         </div>)
    }
}

if (typeof window !== 'undefined') {
    ReactDOM.render((<MainView></MainView>), document.querySelector('.content .bd'))
}
