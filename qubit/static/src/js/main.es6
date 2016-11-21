import { SpoutView } from 'views/spout'
import React from 'react'
import ReactDOM from 'react-dom';
import { bus } from 'bus'

export class MainView extends React.Component {
    componentWillMount() {
        this.setState({
            'nav': 'spout'
        })
    }
    renderViews() {
        return ({
            'spout': <SpoutView></SpoutView>
        }[this.state.nav])
    }
    render () {
        return (
            <div>
              {this.renderViews()}
            </div>)
    }
}

if (typeof window !== 'undefined') {
    ReactDOM.render((<MainView></MainView>), document.querySelector('.content .bd'))
}
