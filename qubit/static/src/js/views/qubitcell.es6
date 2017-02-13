import React from 'react'
import Modal from 'react-modal'
import $ from 'jquery'
import { SocketBus } from 'bus'
import {TSChart } from 'views/vision'
import { qubitModalBus } from 'views/qubitModalForm'

export class QubitCell extends React.Component {
    constructor(props) {
        super(props)
    }
    componentWillMount() {
        var genUrl = (qid) => {
            let host = window.location.host
            return `ws://${ host }/qubit/subscribe/${ qid }/`
        }
        var self = this
        self.setState({
            last: [],
            data: [],
            showCode: false
        })
        self.socketBus = new SocketBus(genUrl(self.props.qid))
        self.bus = self.socketBus.bus
        self.getPeriod()
    }
    componentDidMount() {
        this.listenBus()
    }
    listenBus() {
        let self = this
        if (!self.props.data.store) {
            return
        }
        self.bus.onValue((data)=>{
            let origin = self.state.last
            if (origin.length > 0 && ((new Date(origin[origin.length - 1][0])).getTime() >= (new Date(data.ts).getTime()))) {
                return
            }
            let datum = [data.ts, { mean: data.datum }]
            origin.push(datum)
            if (origin.length > 100) {
                origin.shift()
            }
            self.setState({
                last: origin,
                lastValue: data.datum
            })

        })
    }
    getPeriod() {
        var self = this
        var qid = self.props.qid
        if (!self.props.data.store) {
            return
        }
        $.getJSON('/qubit/' + qid + '/period/seconds/120/', {}, function(resp) {
            if (resp.data.length > 0) {
                self.setState({
                    data: resp.data
                })
            }
        })
    }
    getLast() {
        var self = this
        var qid = self.props.qid
        $.getJSON('/qubit/' + qid + '/period/seconds/1/', {}, function(data) {
            self.setState({
                last: data
            })
        })
    }
    triggerCode() {
        var self = this
        self.setState({
            showCode: !this.state.showCode
        })
    }
    edit() {
        qubitModalBus.push({
            'cmd': 'open',
            'method': 'patch',
            'value': this.props.data
        })
    }
    duplicate() {
        qubitModalBus.push({
            'cmd': 'open',
            'method': 'post',
            'value': this.props.data
        })
    }
    delete() {
        var self = this
        var qid = self.props.qid
        $.ajax({
            url: '/qubit/' + qid + '/',
            data: {},
            method: 'delete',
            success: function() {
                self.props.afterDeleted(qid)
            }})
    }
    showLastData(data) {
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
    showDataChart(data) {
        let style = {
            padding: 0
        }
        if (!data.length > 0) {
            return
        }
        return (
            <div className='chart' style={style}>
              <TSChart
                data={data}
                width={this.props.style.width - 20 || 400 }
                height={ 200 }
                />
            </div>
        )
    }
    detailRender(lst) {
        var self = this
        return lst.map(function(d, i) {
            return (<li key={i}><label>{d}: </label><span>{self.props.data[d].toString()}</span></li>)
        })
    }
    render() {
        let self = this
        return (
            <div className="qubit cell" style={this.props.style || {}}>
              <div className="hd">
                <label>{this.props.data.name}<span>id: {this.props.data.id}</span></label>
                <nav>
                  <ul></ul>
                </nav>
              </div>
              <div className='bd'>
                <ul>
                  {
                      this.detailRender([
                          'flying', 'is_spout', 'is_stem',
                          'entangle', 'store', 'rate'
                      ])
                  }
                </ul>
              </div>
              <div className='ft'>
                <button data-name={this.props.data.name} data-qid={this.props.data.id}
                        onClick={this.getLast.bind(this)}>get last</button>
                <button data-name={this.props.data.name} data-qid={this.props.data.id}
                        onClick={this.delete.bind(this)}>delete</button>
                <button data-name={this.props.data.name} data-qid={this.props.data.id}
                        onClick={this.triggerCode.bind(this)}>monad</button>
                <button data-name={this.props.data.name} data-qid={this.props.data.id}
                        onClick={this.edit.bind(this)}>edit</button>
                <button data-name={this.props.data.name} data-qid={this.props.data.id}
                        onClick={this.duplicate.bind(this)}>duplicate</button>

              </div>
              { self.state.last && self.showDataChart(self.state.last) }
              { self.state.lastValue && self.showLastData(self.state.lastValue) }
              <Modal isOpen={this.state.showCode}>
                <pre>{this.props.data.monad}</pre>
                <button onClick={this.triggerCode.bind(this)}>close</button>
              </Modal>
            </div>
        )
    }
}
