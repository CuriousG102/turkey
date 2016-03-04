var AuditorPastesSpecific = {
    pastes_specific: [],
    log_paste_content: function (e) {
        // e.stopPropagation();
        var pasted_data = e.originalEvent.clipboardData.getData('text');
        this.pastes_specific.push(pasted_data);
    },
    submit_callable: function () {
        return {
            'content':  this.pastes_specific != []
                        ?
                        this.pastes_specific
                        :
                        null
        };
    }
};

var auditor_pastes_specific = Object.create(AuditorPastesSpecific);

$(document).ready(function() {
    $(document).bind("paste", auditor_pastes_specific
                                .log_paste_content
                                .bind(auditor_pastes_specific);
});

overlord.register_auditor('pastes_specific',
                          auditor_pastes_specific
                            .submit_callable
                            .bind(auditor_pastes_specific));