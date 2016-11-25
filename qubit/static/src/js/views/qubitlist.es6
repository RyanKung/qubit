import React from 'react'
import $ from 'jquery'
import ReactDOM from 'react-dom'
import Modal from 'react-modal'
import { QubitForm } from 'views/qubitform'
import { socketStream, updatedSteam } from 'bus'
import { TSChart } from 'views/vision'

export class QubitList extends React.Component {
    componentWillMount() {
        var self = this
        socketStream.onValue(function(value){
            if (value == 'new_stem') {
                self.getData()
            }
        })
        updatedSteam.onValue(function(data) {
            let last = self.state && self.state.last || {}
            last[data.qid] = data.datum
            self.setState({
                last: last
            })
        })
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
            from: from, now: now}, function(data) {
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
    getLast(e) {
        var self = this
        var qid = $(e.target).data('qid')
        $.getJSON('/qubit/' + qid + '/last/', {}, function(data) {
            var last = self.state.last
            last[qid] = data
            self.setState({
                last: last
            })
        })
    }
    delete(e) {
        var self = this
        var qid = $(e.target).data('qid')
        $.ajax({url: '/qubit/' + name + '/',
                data: {},
                method: 'delete',
                success: function(data) {
                    self.getData()
                }})
    }
    renderForm() {
        return (
            <Modal>
              <QubitForm></QubitForm>
            </Modal>
        )
    }
    showData(qid) {
        var self = this
        var data = self.state && self.state.last && self.state.last[qid]
        if (!data) { return '' }
        return (
            <table>
              <tbody>
              <tr>
                {Object.keys(data).map(function(d, i) {
                    return (<th key={i}>{d}</th>)
                })}
              </tr>
              <tr>
                {Object.keys(data).map(function(d, i) {
                    return (<td key={i}>{JSON.stringify(data[d])}</td>)
                })}
            </tr>
                </tbody>
            </table>
        )
    }
    render () {
        var self = this
        return (
            <section className="qubitlist card">
              <div className="hd"><h1>Qubits</h1></div>
              <div className="bd">
                {this.state && this.state.data.map(function(data, i) {
                    return (
                        <div className="qubit cell" key={i}>
                          <div className="hd">
                            <label>{data.name}<span>id: {data.id}</span></label>
                          </div>
                          <div className='bd'>
                            <ul>
                              <li><label>flying: </label><span>{data.flying.toString()}</span></li>
                              <li><label>is_spout: </label><span>{data.is_spout.toString()}</span></li>
                              <li><label>is_stem: </label><span>{data.is_stem.toString()}</span></li>
                              <li><label>entangle: </label><span>{data.entangle}</span></li>
                              <li><label>created at: </label><span>{data.created_at}</span></li>
                            </ul>
                            <pre>{data.monad}</pre>
                          </div>
                          <div className='ft'>
                            <button data-name={data.name} data-qid={data.id}
                                    onClick={self.getLast.bind(self)}>get last</button>
                            <button data-name={data.name} data-qid={data.id}
                                    onClick={self.delete.bind(self)}>delete</button>
                            <div className="last">
                              {self.showData(data.id)}
                            </div>
                            <div className="chart">
                              <TSChart width='500' height='200'></TSChart>
                            </div>
                          </div>
                        </div>
                    )
              })}
            </div>
            </section>
        )
    }
}
