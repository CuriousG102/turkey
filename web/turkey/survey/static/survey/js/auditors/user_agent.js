var AuditorUserAgent = {
    // ua = {},
    uas: "",
    get_user_agent: function() {
        this.uas = navigator.userAgent;
    },
    submit_callable: function() {
        return {
            "user_agent" : this.uas
        };
    }
}

var auditor_user_agent = Object.create(AuditorUserAgent);

$(document).ready(function() {
    auditor_user_agent.get_user_agent();
});

turkey.register_auditor('user_agent',
                          auditor_user_agent
                            .submit_callable
                            .bind(auditor_user_agent));