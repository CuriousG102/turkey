var AuditorKeypressesSpecific = {
    keypresses_specific: [],
    log_keypress_content: function (e) {
        // e.stopPropagation();
        this.keypresses_specific.push(String.fromCharCode(e.keyCode));
    },
    submit_callable: function () {
        return {
            'content':  this.keypresses_specific
        };
    }
};

var auditor_keypresses_specific = Object.create(AuditorKeypressesSpecific);

$(document).ready(function() {
    $(document).keydown(auditor_keypresses_specific
                            .log_keypress_content
                            .bind(auditor_keypresses_specific));
});

overlord.register_auditor('keypresses_specific',
                          auditor_keypresses_specific
                            .submit_callable
                            .bind(auditor_keypresses_specific));