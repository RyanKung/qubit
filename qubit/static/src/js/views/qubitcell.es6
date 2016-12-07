import React from 'react'
import $ from 'jquery'
import ReactDOM from 'react-dom'
import Modal from 'react-modal'
import { SocketBus } from 'bus'
import { TSChart } from 'views/vision'

export class QubitCell extends React.Component {
    componentWillMount() {
        var self = this
        var wsurl = '/qubit/subscribe/%s/'.replace('%s', qid)
        self.setState({
            last: undefined
        })
        self.bus = SocketBus(wsurl).bus
    }
    getLast(e) {
        var self = this
        var qid = $(e.target).data('qid')
        $.getJSON('/qubit/' + qid + '/last/', {}, function(data) {
            self.setState({
                last: data
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
                    this.props.afterDeleted(qid)
                }})
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
    detailRender(lst) {
        var self = this
        return lst.map(function(d, i) {
            return (<li key={i}><label>{d}</lavel><span>{self.props.data[d].toString()}</span></li>)
        })
    }
    render() {
        var self = this
        return (
            <div className="qubit cell">
              <div className="hd">
                <label>{this.props.data.name}<span>id: {this.props.data.id}</span></label>
              </div>
              <div className='bd'>
                <ul>
                  {this.detailRender(['flying', 'is_spout', 'is_stem', 'entangle', 'created_at'])}
                </ul>
                <pre>{this.props.data.monad}</pre>
              </div>
              <div className='ft'>
                <button data-name={this.props.data.name} data-qid={this.props.data.id}
                        onClick={this.getLast.bind(this)}>get last</button>
                <button data-name={this.props.data.name} data-qid={this.props.data.id}
                        onClick={this.delete.bind(this)}>delete</button>
                <div className="last">
                  {this.showData(this.props.data.id)}
                </div>
                <div className="chart">
                  <TSChart width='500' height='200'></TSChart>
                </div>
              </div>
            </div>
        ) 
    }
}
