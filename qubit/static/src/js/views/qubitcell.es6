import React from 'react'
import Modal from 'react-modal'
import $ from 'jquery'
import { SocketBus } from 'bus'

export class QubitCell extends React.Component {
    componentWillMount() {
        var genUrl = (qid) => {
            let host = window.location.host
            let url = `ws://${ host }/qubit/subscribe/${ qid }/`
            return url
        }
        var self = this
        self.setState({
            last: undefined,
            data: [],
            showCode: false
        })
        self.socketBus = new SocketBus(genUrl(self.props.qid))
        self.bus = self.socketBus.bus
        self.getPeriod()
    }
    getPeriod() {
        var self = this
        var qid = self.props.qid
        $.getJSON('/qubit/' + qid + '/period/days/30/', {}, function(data) {
            self.setState({
                data: data
            })
        })
    }
    getLast() {
        var self = this
        var qid = self.props.qid
        $.getJSON('/qubit/' + qid + '/last/', {}, function(data) {
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
    delete() {
        var self = this
        var qid = self.props.qid
        $.ajax({
            url: '/qubit/' + name + '/',
            data: {},
            method: 'delete',
            success: function() {
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
            return (<li key={i}><label>{d}: </label><span>{self.props.data[d].toString()}</span></li>)
        })
    }
    render() {
        return (
            <div className="qubit cell">
              <div className="hd">
                <label>{this.props.data.name}<span>id: {this.props.data.id}</span></label>
                <nav>
                  <ul></ul>
                </nav>
              </div>
              <div className='bd'>
                <ul>
                  {this.detailRender(['flying', 'is_spout', 'is_stem', 'entangle', 'store'])}
                </ul>
              </div>
              <div className='ft'>
                <button data-name={this.props.data.name} data-qid={this.props.data.id}
                        onClick={this.getLast.bind(this)}>get last</button>
                <button data-name={this.props.data.name} data-qid={this.props.data.id}
                        onClick={this.delete.bind(this)}>delete</button>
                <button data-name={this.props.data.name} data-qid={this.props.data.id}
                        onClick={this.triggerCode.bind(this)}>monad</button>

              </div>
              <Modal isOpen={this.state.showCode}>
                <pre>{this.props.data.monad}</pre>
                <button onClick={this.triggerCode.bind(this)}>close</button>
              </Modal>
            </div>
        )
    }
}
