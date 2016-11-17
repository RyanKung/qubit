import React from 'react'
import $ from 'jquery'
import ReactDOM from 'react-dom'

export class SpoutList extends React.Component {
    componentWillMount() {
        this.getData()
    }
    getData() {
        self = this
        $.getJSON('/qubit/spout/', {}, function(data) {
            self.setState({
                data: data.data
            })
        })
    }
    getLast(name) {
        self = this
        $.get('/qubit/spout/' + name + '/last/', {}, function(data) {
            self.setState({
                last: data.data
            })
        })
    }
    render () {
        return (
            <section className="spoutlist card">
              <div className="hd"><h1>Spouts</h1></div>
              <div className="bd">
                {this.state && this.state.data.map(function(data, i) {
                    return (
                        <div className="spout cell" key={data.id}>
                          <div className="hd">
                            <label>{data.name}</label>
                          </div>
                          <div className='bd'>
                            <span>{data.fly}</span>
                            <span>{data.created_at}</span>
                            <detail>{data.body}</detail>
                          </div>
                          <div className='ft'>
                            <span click={this.getLast.bind(this, data.name)}>get last</span>
                            <div>
                              {this.state && this.state.last}
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
