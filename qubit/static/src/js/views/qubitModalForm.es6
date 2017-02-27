import React from 'react'
import Modal from 'react-modal'
import { QubitForm } from 'views/qubitform'
import { bus } from 'bus'
import Bacon from 'baconjs'

export var qubitModalBus = new Bacon.Bus()

export class QubitModalForm extends React.Component {
    constructor(props) {
        super(props)
        this.bus = qubitModalBus
        this.globalBus = bus
    }
    componentWillMount() {
        this.setState({
            'open': false,
            'data': {}
        })
    }
    componentDidMount() {
        let self = this
        self.bus.onValue((msg) => {
            let { cmd, value, method } = msg
            return {
                'open': self.open.bind(self),
                'close': self.close.bind(self),
            }[cmd](value, method)
        })
    }
    close() {
        this.setState({
            'open': false
        })
    }
    afterSubmit() {
        this.close()
        this.props.afterSubmit && this.props.afterSubmit()
    }
    open(data, method) {
        this.setState({
            'open': true,
            'data': data || {},
            'method': method
        })
    }
    setData(data) {
        this.setState({
            'data': data
        })
    }
    render() {
        return (
            <Modal isOpen={ this.state.open }>
              <QubitForm data={ this.state.data }
                         method={ this.state.method || 'post' }
                         cancel={ this.close.bind(this) }
                         submit={ this.afterSubmit.bind(this) }
                         />
            </Modal>
        )
    }
}
