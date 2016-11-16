import React from 'react'
import $ from 'jquery'
import ReactDOM from 'react-dom'
import Form from 'libs/ajaxform'


export class Searcher extends React.Component {
    constructor() {
        super()
    }
    componentWillMount() {
        console.log('init')
        this.setState({
            result: false,
            hint: ''
        })
    }
    success(res, e) {
        var self = this
        if (res.result === "ok") {
            console.log('setting state')
            if (res.data === false) {
                this.setState({
                    hint: 'Can not find data',
                    result: res.data
                })
            } else {
             this.setState({
                 result: res.data
             })
            }
            console.log('setting done')
        } else {
            alert('Failed to fecth data!')
        }
    }
    dataframe(data) {
        return (
            <table className='dataFrame'>
              <tbody>
              <tr>
                {Object.keys(data[0]).map(function(c, i) {
                    return (<th key={i}>{c}</th>)
                })}
            </tr>
                {data.map(function(datum, i) {
                    return (<tr key={i}>
                            {Object.values(datum).map(function(c, i) {
                                return (<td key={i}>{c}</td>)
                            })}
                            </tr>)
                })}
            </tbody>
            </table>
        )
    }
    render() {
        return (
            <section className="card search">
              <div className="hd"><h1>User Searcher</h1></div>
              <Form className="bd" method="get" action="/push_services/admin/peer/search/" success={this.success.bind(this)}>
                <fieldset>
                  <input placeholder="Search via uid/peerid" name="sid" />
                </fieldset>
                <fieldset>
                  <label>Search via</label>
                  <select name="kind">
                    <option value="uid">user id</option>
                    <option value="pid">peer id</option>
                    <option value="sid">services id</option>
                  </select>
                </fieldset>
                <fieldset>
                  <input name="submit" type="submit" value="Search!" />
                </fieldset>
              </Form>
              <div className="ft">
                <h2>result</h2>
                <em>{this.state.hint}</em>
                {this.state.result && this.dataframe(this.state.result)}
              </div>
            </section>)
    }
}
