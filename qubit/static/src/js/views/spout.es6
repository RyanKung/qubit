import React from 'react'
import $ from 'jquery'
import ReactDOM from 'react-dom'
import Modal from 'react-modal'
import { SpoutForm } from 'views/spoutform'
import { SpoutList } from 'views/spoutlist'


export class SpoutView extends React.Component {
    render () {
        return (
            <section className="spout">
              <div className="hd"></div>
              <div className="bd"></div>
              <SpoutList></SpoutList>
              <SpoutForm></SpoutForm>
            </section>
        )
    }
}
