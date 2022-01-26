new Vue({
    el: '#ticket_app',
    data: {
        tickets: []
    },
    created: function () {
        const vm = this;
        axios.get('/api/messages')
            .then(function (response) {
            vm.tickets = response.data
            })
    }
})
