var AuditorOnFocusTime = {
    start_date: new Date(),
    hidden: null,
    visibility_change: null,
    on_focus_time: 0,
    last_focus_time: this.start_date, // switch in focus
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
    log_on_focus_time: function (e) {
        if(document[this.hidden]) {
            var focus_change_time = (new Date()).getTime();
            this.on_focus_time += focus_change_time - this.last_focus_time;  
        } else {
            this.last_focus_time = (new Date()).getTime(); 
        }
    },
    submit_callable: function () {
        return {
            'milliseconds': this.on_focus_time
        };
    }
};

var auditor_on_focus_time = Object.create(AuditorOnFocusTime);
auditor_on_focus_time.setup();

$(document).ready(function() {
    document.addEventListener(  visibility_change,
                                function() {
                                    auditor_on_focus_time.hidden = hidden;
                                    auditor_on_focus_time.log_on_focus_time;
                                },
                                false);
});

overlord.register_auditor('on_focus_time',
                          auditor_on_focus_time
                            .submit_callable
                            .bind(auditor_on_focus_time));