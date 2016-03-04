var AuditorKeypressesTotal = {
    keypresses_total: 0,
    log_keypress_event: function (e) {
        // e.stopPropagation();
        this.keypresses_total += 1;
    },
    submit_callable: function () {
        return {
            'count': this.keypresses_total
        };
    }
};

var auditor_keypresses_total = Object.create(AuditorKeypressesTotal);

$(document).ready(function() {
    $(document).keydown(auditor_keypresses_total
                            .log_keypress_event
                            .bind(auditor_keypresses_total));
});

overlord.register_auditor('keypresses_total',
                          auditor_keypresses_total
                            .submit_callable
                            .bind(auditor_keypresses_total));