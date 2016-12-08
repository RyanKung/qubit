import { QubitView } from 'views/qubit'
import React from 'react'
import ReactDOM from 'react-dom'

export class MainView extends React.Component {
    componentWillMount() {
        this.setState({
            'nav': 'qubit'
        })
    }
    renderViews() {
        return ({
            'qubit': <QubitView></QubitView>
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
