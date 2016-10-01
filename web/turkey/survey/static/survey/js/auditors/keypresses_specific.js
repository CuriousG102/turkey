var AuditorKeypressesSpecific = {
    start_date: new Date(),
    keypresses_specific: [],
    log_keypress_content: function (e) {
        this.keypresses_specific.push({
            'key' : String.fromCharCode(e.which),
            'time': (new Date()).getTime() - this.start_date.getTime()
        });
    },
    submit_callable: function () {
        return this.keypresses_specific;
    }
};

var auditor_keypresses_specific = Object.create(AuditorKeypressesSpecific);

$(document).ready(function() {
    $(document).keyup(auditor_keypresses_specific
                            .log_keypress_content
                            .bind(auditor_keypresses_specific));
});

turkey.register_auditor('keypresses_specific',
                          auditor_keypresses_specific
                            .submit_callable
                            .bind(auditor_keypresses_specific));