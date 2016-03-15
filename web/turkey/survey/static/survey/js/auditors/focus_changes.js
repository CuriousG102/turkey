var AuditorFocusChanges = {
    start_date: new Date(),
    hidden: null,
    visibility_change: null,
    focus_changes: [],
    setup: function() {
        if (typeof document.hidden !== "undefined") {
            this.hidden = "hidden";
            this.visibility_change = "visibilitychange";
        } else if (typeof document.mozHidden !== "undefined") {
            this.hidden = "mozHidden";
            this.visibility_change = "mozvisibilitychange";
        } else if (typeof document.msHidden !== "undefined") {
            this.hidden = "msHidden";
            this.visibility_change = "msvisibilitychange";
        } else if (typeof document.webkitHidden !== "undefined") {
            this.hidden = "webkitHidden";
            this.visibility_change = "webkitvisibilitychange";
        }
    },
    log_focus_changes: function (e) {
        if(document[this.hidden]) {
            var focus_change_time = (new Date()).getTime();
            focus_changes.push(focus_change_time - start_date.getTime());
        }
    },
    submit_callable: function () {
        return {
            'times': this.focus_changes
        };
    }
};

var auditor_focus_changes = Object.create(AuditorFocusChanges);
auditor_focus_changes.setup();

document.addEventListener(  auditor_focus_changes.visibility_change,
                            auditor_focus_changes
                                .log_focus_changes
                                .bind(auditor_focus_changes),
                            false);

overlord.register_auditor('focus_changes',
                          auditor_focus_changes
                            .submit_callable
                            .bind(auditor_focus_changes));