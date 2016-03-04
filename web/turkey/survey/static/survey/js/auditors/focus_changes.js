var AuditorFocusChanges = {
    start_date: new Date(),
    hidden: null,
    focus_changes: [],
    log_focus_changes: function (e) {
        if(document[this.hidden]) {
            var focus_change_time = (new Date()).getTime();
            focus_changes.push(focus_change_time - start_date.getTime());
        }
    },
    submit_callable: function () {
        return {
            'times': this.focus_changes != []
                            ?
                            this.focus_changes
                            :
                            null
        };o
    }
};

var auditor_focus_changes = Object.create(AuditorFocusChanges);

$(document).ready(function() {
    document.addEventListener(  visibility_change,
                                function() {
                                    auditor_focus_changes.hidden = hidden;
                                    auditor_focus_changes.log_focus_changes;
                                },
                                false);
});

overlord.register_auditor('focus_changes',
                          auditor_focus_changes
                            .submit_callable
                            .bind(auditor_focus_changes));