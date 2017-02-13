import React from 'react'
import $ from 'jquery'
import ReactDOM from 'react-dom'
import Modal from 'react-modal'
import { QubitForm } from 'views/qubitform'
import { QubitCell } from 'views/qubitcell'
import { updateBus } from 'bus'

export class StemList extends React.Component {
    componentWillMount() {
        this.setState({
            last: {},
            data: []
        })
        this.getData()
    }
    componentDidMount() {
        let self = this
        updateBus.onValue((v) => {
            if (v.stem === true) {
                self.getData()
            }
        })
    }
    getStates(qid) {
        var now = (new Date()).getTime()
        var from = now - 3600
        $.getJSON('/qubit/state/' + qid, {
            from: from,
            now: now
        }, function() {

        })
    }
    getData() {
        var self = this
        $.getJSON('/qubit/stem/', {}, function(data) {
            self.setState({
                data: data.data
            })
        })
    }
    renderForm() {
        return (
            <Modal>
              <QubitForm></QubitForm>
            </Modal>
        )
    }
    refresh() {
        this.getData()
    }
    render () {
        var self = this
        return (
            <section className="qubitlist" style={{width: '20%'}}>
              <div className="hd"><h1>Qubits</h1></div>
              <div className="bd">
                {this.state && this.state.data.map(function(data, i) {
                    return (
                        <QubitCell
                          key={i} data={data}
                          style={{width: '100%', marginTop: 10}}
                          qid={data.id}
                          afterDeleted={self.refresh.bind(self)}></QubitCell>
                    )
                })}
            </div>
            </section>
        )
    }
}
