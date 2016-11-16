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
    render () {
        return (
            <section className="spoutlist card">
              <div className="hd"><h1>Spouts</h1></div>
              <div className="bd">
                {this.state && this.state.data.map(function(data, i) {
                    return (
                        <div key={i}>
                          <label>{data.name}</label>
                          <div>{data.body}</div>
                        </div>
                    )
              })}
            </div>
            </section>
        )
    }
}
