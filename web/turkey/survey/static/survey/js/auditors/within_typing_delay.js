var AuditorWithinTypingDelay = {
    start_date: new Date(),
    first_typing_event_date: null,
    // within_typing_delay: false,
    typing_delay: 10000, // milliseconds
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
            'within_delay': this.first_typing_event_date
                            ?
                            ((this.first_typing_event_date.getTime() -
                                this.start_date.getTime()) < this.typing_delay).toString()
                            :
                            null
        };
    }
};

var auditor_within_typing_delay = Object.create(AuditorWithinTypingDelay);

$(document).ready(function() {
    $(document).keydown(auditor_within_typing_delay
                          .log_keydown_typing_event
                          .bind(auditor_within_typing_delay));
});

turkey.register_auditor('within_typing_delay',
                          auditor_within_typing_delay
                            .submit_callable
                            .bind(auditor_within_typing_delay));