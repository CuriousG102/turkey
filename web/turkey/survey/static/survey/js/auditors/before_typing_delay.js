var AuditorBeforeTypingDelay = {
    start_date: new Date(),
    first_typing_event_date: null,
    log_keydown_typing_event: function (e) {
        // there has not yet been a typing event recorded
        // and this typing event qualifies for recording
        // because it is one of the letters of the alphabet
        if (!this.first_typing_event_date
            && e.keyCode >= 65
            && e.keyCode <= 90) {
            this.first_typing_event_date = new Date();
        }
    },
    submit_callable: function () {
        return {
            'did_type': this.first_typing_event_date ? true : false,
            'milliseconds': this.first_typing_event_date.getTime() -
                            this.start_date.getTime()
        };
    }
};

var auditor_before_typing_delay = Object.create(AuditorBeforeTypingDelay);

$(document).ready(function() {
    $(document).keydown(auditor_before_typing_delay
                          .log_keydown_typing_event
                          .bind(auditor_before_typing_delay));
});

overlord.register_auditor('before_typing_delay',
                          auditor_before_typing_delay
                            .submit_callable
                            .bind(auditor_before_typing_delay));