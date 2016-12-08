import React from 'react'
import $ from 'jquery'
import ReactDOM from 'react-dom'
import Modal from 'react-modal'
import { QubitForm } from 'views/qubitform'
import { QubitCell } from 'views/qubitcell'

export class QubitList extends React.Component {
    componentWillMount() {
        this.setState({
            last: {},
            data: []
        })
        this.getData()
    }
    getStates(qid) {
        var now = (new Date()).getTime()
        var from = now - 3600
        $.getJSON('/qubit/state/' + qid, {
            from: from, now: now}, function() {

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
            <section className="qubitlist">
              <div className="hd"><h1>Qubits</h1></div>
              <div className="bd">
                {this.state && this.state.data.map(function(data, i) {
                    return (
                        <QubitCell key={i} data={data} qid={data.id} afterDeleted={self.refresh}></QubitCell>
                    )
                })}
            </div>
            </section>
        )
    }
}
