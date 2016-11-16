import React from 'react'
import AjaxForm from 'libs/ajaxForm'



export class Searcher extends React.Component {
    success(res, e) {
        window.alert('success')
    }
    render() {
        return (
                <AjaxForm method="post" action="/admin/peer/search" success={this.success}>
                <p>test</p>
                </AjaxForm>
        )
    }
}
