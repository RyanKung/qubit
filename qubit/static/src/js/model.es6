import $ from 'jquery'

export var APIs = {
    qubitList: function(measure, callback) {
        $.getJSON(`/qubit/entangle/${ measure }/tree/`,
                  {}, function(resp) {
                      callback.call(this, resp)
                  })
    },
    stem: function(callback) {
        $.getJSON('/qubit/stem/',
                  {}, function(resp) {
                      callback.call(this, resp)
                  })
    },
    state: function(qid, data, callback) {
        $.getJSON(`/qubit/state/${ qid }`,
                  data, function(resp) {
                      callback.call(this, resp)
                  })
    },
    period: function(qid, period, range, callback) {
        $.getJSON(`/qubit/${ qid }/period/${ period }/${ range }/`,
                  {}, function(data) {
                      callback.call(this, data)
                  })
    }

}
