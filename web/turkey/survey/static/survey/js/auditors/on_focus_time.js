var AuditorOnFocusTime = {
    start_date: new Date(),
    hidden: null,
    on_focus_time: 0,
    last_focus_time: null, // switch in focus
    log_on_focus_time: function (e) {
        if(document[this.hidden]) {
            var focus_change_time = (new Date()).getTime();
            this.on_focus_time += focus_change_time - this.last_focus_time;
        } else {
            this.last_focus_time = (new Date()).getTime();
        }
    },
    submit_callable: function () {
        var focus_change_time = (new Date()).getTime();
        this.on_focus_time += focus_change_time - this.last_focus_time;

        return {
            'milliseconds': this.on_focus_time
        };
    }
};

var auditor_on_focus_time = Object.create(AuditorOnFocusTime);
auditor_on_focus_time.hidden = hidden;
auditor_on_focus_time.last_focus_time = auditor_on_focus_time.start_date.getTime();

document.addEventListener(  visibility_change,
                            auditor_on_focus_time
                                .log_on_focus_time
                                .bind(auditor_on_focus_time),
                            false);

turkey.register_auditor('on_focus_time',
                          auditor_on_focus_time
                            .submit_callable
                            .bind(auditor_on_focus_time));