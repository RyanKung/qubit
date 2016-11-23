import React from 'react'
import $ from 'jquery'
import ReactDOM from 'react-dom'
import Modal from 'react-modal'
import { SpoutForm } from 'views/spoutform'
import { socketStream } from 'bus'

export class SpoutList extends React.Component {
    componentWillMount() {
        var self = this
        socketStream.onValue(function(value){
            if (value == 'new_stem') {
                self.getData()
            }
        })
        this.setState({
            last: {},
            data: []
        })
        this.getData()
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
        var name = $(e.target).attr('name')
        $.getJSON('/qubit/' + name + '/last/', {}, function(data) {
            var last = self.state.last
            last[name] = data
            self.setState({
                last: last
            })
        })
    }
    delete(e) {
        var self = this
        var name = $(e.target).attr('name')
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
              <SpoutForm></SpoutForm>
            </Modal>
        )
    }
    showData(name) {
        var self = this
        var data = self.state && self.state.last && self.state.last[name]
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
        console.log(self)
        return (
            <section className="spoutlist card">
              <div className="hd"><h1>Spouts</h1></div>
              <div className="bd">
                {this.state && this.state.data.map(function(data, i) {
                    return (
                        <div className="spout cell" key={i}>
                          <div className="hd">
                            <label>{data.name}</label>
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
                            <button name={data.name}
                                    onClick={self.getLast.bind(self)}>get last</button>
                            <button name={data.name}
                                    onClick={self.delete.bind(self)}>delete</button>
                            <div>
                              {self.showData(data.name)}
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
