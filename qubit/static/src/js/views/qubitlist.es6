import React from 'react'
import ReactDOM from 'react-dom'
import Modal from 'react-modal'
import { QubitForm } from 'views/qubitform'
import { QubitCell } from 'views/qubitcell'
import { updateBus } from 'bus'
import { APIs } from 'model'

export class StemList extends React.Component {
    componentWillMount() {
        this.setState({
            last: {},
            data: [],
            selected: undefined
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
        APIs.state(qid, {
            from: from,
            now: now
        }, function() {
            
        })
    }
    getData() {
        var self = this
        APIs.stem(function(data) {
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
    selected(qid) {
        this.setState({
            selected: qid
        })
        updateBus.push({
            measureOn: 'Stem:' + qid
        })
    }
    render () {
        var self = this
        return (
            <section className="qubitlist" style={{width: '20%'}}>
              <div className="hd"><h1>Qubits</h1></div>
              <div className="bd">
                {self.state && self.state.data.map(function(data, i) {
                    return (
                        <QubitCell
                          onClick={self.selected.bind(self, data.id)}
                          key={i} data={data}
                          selected={ data.id===self.state.selected }
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
