import React from 'react'
import { QubitCell } from 'views/qubitcell'
import { updateBus } from 'bus'
import { APIs } from 'model'

export class MeasureList extends React.Component {
    componentWillMount() {
        this.setState({
            qubits: []
        })
        this.measureOn = undefined
    }
    componentDidMount() {
        let self = this
        updateBus.onValue((v) => {
            if (v.stem === false) {  // for refresh
                self.getQubitList()
            }
            if (v.measureOn !== undefined && v.measureOn !== self.state.measureOn) {
                self.measureOn = v.measureOn
                self.getQubitList()
            }
        })
    }
    getQubitList() {
        let self = this
        APIs.qubitList(self.measureOn, function(data) {
            return self.setState({
                qubits: data.data
            })
        })
    }
    renderQubitLayer(layer, i) {
        let self = this
        return (
            <div key={i} className='QubitLayer layer'>
              {layer.map((q, i)=>{
                  return (
                      <QubitCell data={q}
                                 qid={q.id}
                                 key={i}
                                 style={self.qubitStyle()}>
                      </QubitCell>)
              })}
            </div>
        )
    }
    style() {
        return {
            float: 'right',
            marginTop: 50,
            width: '78%'
        }
    }
    qubitStyle() {
        return {
            width: '100%',
            marginTop: 10
        }
    }
    render() {
        let self = this
        return (
            <div style={self.style()}>
              { self.state.qubits.map((d, i) => {
                  return self.renderQubitLayer(d, i)
              }) }
            </div>
        )
    }
    
}
