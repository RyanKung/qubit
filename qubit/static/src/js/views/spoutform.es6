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
    success(res, e, cb) {
        if (res.result == "ok") {
            console.log(res.data)
            this.setState({
                result: 'successed! spout id: ' + res.data
            })
            this.props.submit && this.props.submit(this.data)
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
        return JSON.stringify(resp)
    }
    render() {
        return (
            <section className="card">
              <div className="hd"><h1>New Spout</h1></div>
              <Form className="bd" action="/qubit/"
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
                  <label>
                    <span>is spout</span>
                    <input name='is_spout' type='checkbox' />
                    </label>
                  <label>
                    <span>is stem</span>
                    <input name='is_stem' type='checkbox' />
                    </label>
                </fieldset>
                <fieldset className="long">
                  <label>monad</label>
                  <textarea name="monad" placeholder="monad"></textarea>
                </fieldset>
                <fieldset className="long">
                  <label>comment</label>
                  <textarea name="comment" placeholder="coment"></textarea>
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
