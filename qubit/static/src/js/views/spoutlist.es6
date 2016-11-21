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
            if (value == 'newSpout') {
                self.getData()
            }
        })
        this.setState({
            last: {}
        })
        this.getData()
    }
    getData() {
        var self = this
        $.getJSON('/qubit/spout/', {}, function(data) {
            self.setState({
                data: data.data
            })
        })
    }
    getLast(e) {

        var self = this
        var name = $(e.target).attr('name')
        $.get('/qubit/spout/' + name + '/last/', {}, function(data) {
            var last = self.state.last
            last[name] = JSON.stringify(data)
            self.setState({
                last: last
            })
        })
    }
    delete(e) {
        var self = this
        var name = $(e.target).attr('name')
        $.ajax({url: '/qubit/spout/' + name + '/',
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
                            <span>{data.fly}</span>
                            <span>{data.created_at}</span>
                            <detail>{data.body}</detail>
                          </div>
                          <div className='ft'>
                            <button name={data.name}
                                    onClick={self.getLast.bind(self)}>get last</button>
                            <button name={data.name}
                                    onClick={self.delete.bind(self)}>delete</button>
                            <div>
                              {self.state && self.state.last[data.name]}
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
