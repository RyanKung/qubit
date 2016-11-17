import React from 'react'
import $ from 'jquery'
import ReactDOM from 'react-dom'
import Form from 'libs/ajaxform'


export class SpoutForm extends React.Component {
    componentWillMount() {
        this.setState({
            result: false,
            hint: ''
        })
    }
    success(res, e) {
        if (res.result == "ok") {
            console.log(res.data)
            this.setState({
                result: 'successed! spout id: ' + res.data
            })
            window.alert(this.state.result)
        } else {
            window.alert('failed to post data')
        }
    }
    toDict(data) {
        return data.reduce(function(x, y, i) {
            x[y.name] = y.value
            return x
        }, {})
    }
    series($dom) {
        let resp = this.toDict($dom.serializeArray())
        console.log(resp)
        return JSON.stringify(resp)
    }
    render() {
        return (
            <section className="card">
              <div className="hd"><h1>New Spout</h1></div>
              <Form className="bd" action="/qubit/spout/"
                    series={this.series.bind(this)}
                    contentType='application/json'
                    success={this.success.bind(this)}
                    method='post'>
                <fieldset>
                  <input placeholder="name" name="name" />
                  <input placeholder='rate (ms)' name='rate' type='number' />
                </fieldset>
                <fieldset>
                  <label>
                    <span>flying</span>
                    <input placeholder='flying' name='flying' type='checkbox' />
                    </label>
                </fieldset>

                <fieldset className="long">
                  <label>body</label>
                  <textarea name="body" placeholder="body"></textarea>
                </fieldset>
                <fieldset className="submit block">
                  <input name="submit" type="submit" value="submmit" />
                </fieldset>
              </Form>

              <div className="ft">
                <em>{this.state.hint}</em>
                <div>{this.state.result}</div>
              </div>
            </section>
        )
    }
}
