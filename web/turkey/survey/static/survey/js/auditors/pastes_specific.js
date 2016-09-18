var AuditorPastesSpecific = {
    start_date: new Date(),
    pastes_specific: [],
    log_paste_content: function (e) {
        this.pastes_specific.push({
            'data' : e.originalEvent.clipboardData.getData('text'),
            'time' : (new Date()).getTime() - this.start_date.getTime()
        });
    },
    submit_callable: function () {
        return this.pastes_specific;
    }
};

var auditor_pastes_specific = Object.create(AuditorPastesSpecific);

$(document).ready(function() {
    $(document).bind("paste", 
        function(e) {
            auditor_pastes_specific
                .log_paste_content
                .bind(auditor_pastes_specific)(e);
        }
    )
});

turkey.register_auditor('pastes_specific',
                          auditor_pastes_specific
                            .submit_callable
                            .bind(auditor_pastes_specific));