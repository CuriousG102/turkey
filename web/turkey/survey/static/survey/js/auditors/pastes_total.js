var AuditorPastesTotal = {
    pastes_total: 0,
    log_paste_event: function (e) {
        // e.stopPropagation();
        this.pastes_total += 1;
    },
    submit_callable: function () {
        return {
            'count': this.pastes_total
        };
    }
};

var auditor_pastes_total = Object.create(AuditorPastesTotal);

$(document).ready(function() {
    $(document).bind("paste", auditor_pastes_total
                                .log_paste_event
                                .bind(auditor_pastes_total));
});

overlord.register_auditor('pastes_total',
                          auditor_pastes_total
                            .submit_callable
                            .bind(auditor_pastes_total));