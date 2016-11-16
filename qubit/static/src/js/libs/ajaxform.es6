import React from 'react'
import ReactDOM from 'react-dom'
import $ from 'jquery'

export default React.createClass({
    submit: function(e) {
        e.preventDefault()
        let $dom = $(ReactDOM.findDOMNode(this));
        let self=this
        if (this.props.series) {
            var data = this.props.series($dom)
        } else {
            var data = $dom.serialize()
        }
        console.log(data)
        $.ajax({
            url: $dom.attr('action'),
            type: $dom.attr('method'),
            data: data,
            dataType: 'json',
            contentType: self.props.contentType || 'application/x-www-form-urlencoded',
            success: function(res) {
                self.props.success && self.props.success(res, e)
            }
        })
    },
    render: function() {
        return (<form onSubmit={this.submit} method={this.props.method} action={this.props.action}>
                {this.props.children}
                </form>)
    }
})
