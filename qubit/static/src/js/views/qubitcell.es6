import React from 'react'
import $ from 'jquery'
import ReactDOM from 'react-dom'
import Modal from 'react-modal'
import { socketStream, updatedSteam } from 'bus'
import { TSChart } from 'views/vision'

export class QubitCell extends React.Component {
    componentWillMount() {
        var self = this
        self.setState({
            last: undefined
        })
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
    render() {
        return (
            <div className="qubit cell">
              <div className="hd">
                <label>{this.props.data.name}<span>id: {this.props.data.id}</span></label>
              </div>
              <div className='bd'>
                <ul>
                  <li><label>flying: </label><span>{this.props.data.flying.toString()}</span></li>
                  <li><label>is_spout: </label><span>{this.props.data.is_spout.toString()}</span></li>
                  <li><label>is_stem: </label><span>{this.props.data.is_stem.toString()}</span></li>
                  <li><label>entangle: </label><span>{this.props.data.entangle}</span></li>
                  <li><label>created at: </label><span>{this.props.data.created_at}</span></li>
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
